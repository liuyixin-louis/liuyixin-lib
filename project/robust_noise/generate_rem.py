import os
import pickle
import argparse
import numpy as np
import torch
from tqdm import tqdm
import utils
import attacks
import time
from torch.optim.lr_scheduler import ExponentialLR
import torch.distributed as dist
# from robust_noise.attack import RobustMiniNonMaxPGDDefender
# os.environ['CUDA_VISIBLE_DEVICES']='0,1,2,3,4,5,6,7'

def get_args():
    parser = argparse.ArgumentParser()
    utils.add_shared_args(parser)

    parser.add_argument('--perturb-freq', type=int, default=1,
                        help='set the perturbation frequency')
    parser.add_argument('--report-freq', type=int, default=500,
                        help='set the report frequency')
    parser.add_argument('--save-freq', type=int, default=5000,
                        help='set the checkpoint saving frequency')

    parser.add_argument('--samp-num', type=int, default=1,
                        help='set the number of samples for calculating expectations')

    parser.add_argument('--atk-pgd-radius', type=float, default=0,
                        help='set the adv perturbation radius in minimax-pgd')
    parser.add_argument('--atk-pgd-steps', type=int, default=0,
                        help='set the number of adv iteration steps in minimax-pgd')
    parser.add_argument('--atk-pgd-step-size', type=float, default=0,
                        help='set the adv step size in minimax-pgd')
    parser.add_argument('--atk-pgd-random-start', action='store_true',
                        help='if select, randomly choose starting points each time performing adv pgd in minimax-pgd')

    parser.add_argument('--pretrain', action='store_true',
                        help='if select, use pre-trained model')
    parser.add_argument('--pretrain-path', type=str, default=None,
                        help='set the path to the pretrained model')

    parser.add_argument('--resume', action='store_true',
                        help='set resume')
    parser.add_argument('--resume-step', type=int, default=None,
                        help='set which step to resume the model')
    parser.add_argument('--resume-dir', type=str, default=None,
                        help='set where to resume the model')
    parser.add_argument('--resume-name', type=str, default=None,
                        help='set the resume name')

    parser.add_argument('--uniform_scale', type=float, default=2.0,
                        help='random uniform attack')

    parser.add_argument("--attacker",type=str,default="pgd",help="the attacker type")

    parser.add_argument("--extra_data",type=str,default=None,help="extra data")

    parser.add_argument("--defense_model_adv",type=str,default="pgd",help="the attacker type that model in the defender")

    parser.add_argument("--total_train_epoch",type=int,default=10,help="the toatl epoch of training")

    # parser.add_argument("--defense_model_adv",type=str,default="pgd",help="the attacker type that model in the defender")
    # parser.add_argument("--defense_model_adv",type=str,default="pgd",help="the attacker type that model in the defender")

    return parser.parse_args()


def load_pretrained_model(model, arch, pre_state_dict):
    target_state_dict = model.state_dict()

    for name, param in pre_state_dict.items():
        if (arch=='resnet18') and ('linear' in name): continue
        target_state_dict[name].copy_(param)


def regenerate_def_noise(def_noise, model, criterion, loader, defender, cpu):
    for x, y, ii in tqdm(loader):
        if not cpu: x, y = x.cuda(), y.cuda()
        # delta = torch.zeros_like(x.data)
        delta = defender.perturb(model, criterion, x, y)
        # def_noise[ii] = delta.cpu().numpy()
        def_noise[ii] = (delta.cpu().numpy() * 255).round().astype(np.int8)


def save_checkpoint(save_dir, save_name, model, optim, log, def_noise=None):
    torch.save({
        'model_state_dict': utils.get_model_state(model),
        'optim_state_dict': optim.state_dict(),
        }, os.path.join(save_dir, '{}-model.pkl'.format(save_name)))
    with open(os.path.join(save_dir, '{}-log.pkl'.format(save_name)), 'wb') as f:
        pickle.dump(log, f)
    if def_noise is not None:
        # def_noise = (def_noise * 255).round()
        # def_noise = def_noise * 255
        # def_noise = def_noise.round()
        # assert (def_noise.max()<=127 and def_noise.min()>=-128)
        # def_noise = def_noise.astype(np.int8)
        with open(os.path.join(save_dir, '{}-def-noise.pkl'.format(save_name)), 'wb') as f:
            pickle.dump(def_noise, f)
    # print('checkpoint存储成功！')

def main(args, logger):
    ''' init model / optim / loss func '''
    model = utils.get_arch(args.arch, args.dataset)
    optim = utils.get_optim(
        args.optim, model.parameters(),
        lr=args.lr, weight_decay=args.weight_decay, momentum=args.momentum)
    criterion = torch.nn.CrossEntropyLoss()

    ''' get Tensor train loader '''
    # trainset = utils.get_dataset(args.dataset, root=args.data_dir, train=True)
    # trainset = utils.IndexedTensorDataset(trainset.x, trainset.y)
    # train_loader = utils.Loader(
    #     trainset, batch_size=args.batch_size, shuffle=True, drop_last=True)
    train_loader = utils.get_indexed_t ensor_loader(
        args.dataset, batch_size=args.batch_size, root=args.data_dir, train=True,load_other=True)

    ''' get train transforms '''
    train_trans = utils.get_transforms(
        args.dataset, train=True, is_tensor=True)

    ''' get (original) test loader '''
    test_loader = utils.get_indexed_loader(
        args.dataset, batch_size=args.batch_size, root=args.data_dir, train=False)

    if args.attacker == "random":
        attacker = attacks.RandomUniformAttacker(
            radius=args.atk_pgd_radius,
            norm_type='l-infty',
            uniform_scale=args.uniform_scale
        )

    elif args.attacker == "pgd":
        attacker = attacks.PGDAttacker(
            radius=args.atk_pgd_radius,
            steps=args.atk_pgd_steps,
            step_size=args.atk_pgd_step_size,
            random_start=args.atk_pgd_random_start,
            norm_type='l-infty',
            ascending=True,
        )

    # if args.defender == "baseline":
    defender = attacks.RobustMiniPGDAttackDefender(
        samp_num         = args.samp_num,
        trans            = train_trans,
        radius           = args.pgd_radius,
        steps            = args.pgd_steps,
        step_size        = args.pgd_step_size,
        random_start     = args.pgd_random_start,
        atk_radius       = args.atk_pgd_radius,
        atk_steps        = args.atk_pgd_steps,
        atk_step_size    = args.atk_pgd_step_size,
        atk_random_start = args.atk_pgd_random_start,
        attacker         = args.defense_model_adv
    )
    # elif


    ''' initialize the defensive noise (for unlearnable examples) '''
    data_nums = len( train_loader.loader.dataset )
    if args.dataset == 'cifar10' or args.dataset == 'cifar100':
        # def_noise = np.zeros([data_nums, 3, 32, 32], dtype=np.float16)
        def_noise = np.zeros([data_nums, 3, 32, 32], dtype=np.int8)
    elif args.dataset == 'tiny-imagenet':
        # def_noise = np.zeros([data_nums, 3, 64, 64], dtype=np.float16)
        def_noise = np.zeros([data_nums, 3, 64, 64], dtype=np.int8)
    elif args.dataset == 'imagenet-mini':
        # def_noise = np.zeros([data_nums, 3, 256, 256], dtype=np.float16)
        def_noise = np.zeros([data_nums, 3, 256, 256], dtype=np.int8)
    elif "mnist" in args.dataset:
        def_noise = np.zeros([data_nums, 1, 28, 28], dtype=np.int8)
    elif "svhn" in args.dataset:
        def_noise = np.zeros([data_nums, 3, 32, 32], dtype=np.int8)
    else:
        raise NotImplementedError

    start_step = 0
    log = dict()

    if not args.cpu:
        model.cuda()
        criterion = criterion.cuda()

    if args.pretrain:
        state_dict = torch.load(args.pretrain_path)
        load_pretrained_model(model, args.arch, state_dict['model_state_dict'])
        del state_dict

    if args.resume:
        start_step = args.resume_step

        state_dict = torch.load( os.path.join(args.resume_dir, '{}-model.pkl'.format(args.resume_name)) )
        model.load_state_dict( state_dict['model_state_dict'] )
        optim.load_state_dict( state_dict['optim_state_dict'] )
        del state_dict

        with open(os.path.join(args.resume_dir, '{}-log.pkl'.format(args.resume_name)), 'rb') as f:
            log = pickle.load(f)

        with open(os.path.join(args.resume_dir, '{}-def-noise.pkl'.format(args.resume_name)), 'rb') as f:
            # def_noise = pickle.load(f).astype(np.float16) / 255
            def_noise = pickle.load(f)

    if args.parallel:
        # torch.distributed.init_process_group(backend="nccl")
        # import torch.nn.parallel as parallel
        # model = nn.parallel.DistributedDataParallel(model, device_ids=[args.local_rank], output_device=args.local_rank, find_unused_parameters=True)
        model = torch.nn.DataParallel(model)
    start_time = time.time()
    for step in tqdm(range(start_step, args.train_steps)):
        lr = args.lr * (args.lr_decay_rate ** (step // args.lr_decay_freq))
        for group in optim.param_groups:
            group['lr'] = lr
        ######## update noise ##############
        x, y, ii = next(train_loader)
        if not args.cpu:
            x, y = x.cuda(), y.cuda()

        s1 = time.time()
        if (step+1) % args.perturb_freq == 0:
            delta = defender.perturb(model, criterion, x, y) # 基于PGD生成噪声
            # def_noise[ii] = delta.cpu().numpy()
            def_noise[ii] = (delta.cpu().numpy() * 255).round().astype(np.int8)
            s2 = time.time()
            # print(f"{s2-s1}s use to produce defense noise!")

        ######## update model theta ##############
        if args.cpu:
            # def_x = train_trans(x + torch.tensor(def_noise[ii])*255)
            def_x = train_trans(x + torch.tensor(def_noise[ii]))
        else:
            # def_x = train_trans(x + torch.tensor(def_noise[ii]).cuda()*255)
            def_x = train_trans(x + torch.tensor(def_noise[ii]).cuda())
        def_x.clamp_(-0.5, 0.5)

        s3 = time.time()
        adv_x = attacker.perturb(model, criterion, def_x, y)
        s4 = time.time()
        # print(f"{s4-s3}s use to conduct pgd attack to produce adv example!")

        model.train()
        _y = model(adv_x)
        def_acc = (_y.argmax(dim=1) == y).sum().item() / len(x)
        def_loss = criterion(_y, y)
        optim.zero_grad()
        def_loss.backward()
        optim.step()

        utils.add_log(log, 'def_acc', def_acc)
        utils.add_log(log, 'def_loss', def_loss.item())

        if (step+1) % args.save_freq == 0:
            save_checkpoint(
                args.save_dir, '{}-ckpt-{}'.format(args.save_name, step+1),
                model, optim, log, def_noise)

        if (step+1) % args.report_freq == 0:
            test_acc, test_loss = utils.evaluate(model, criterion, test_loader, args.cpu)
            utils.add_log(log, 'test_acc', test_acc)
            utils.add_log(log, 'test_loss', test_loss)

            logger.info('step [{}/{}]:'.format(step+1, args.train_steps))
            logger.info('def_acc {:.2%} \t def_loss {:.3e}'
                        .format( def_acc, def_loss.item() ))
            logger.info('test_acc  {:.2%} \t test_loss  {:.3e}'
                        .format( test_acc, test_loss ))
            logger.info('')

    logger.info('Noise generation started')

    regenerate_def_noise(
        def_noise, model, criterion, train_loader, defender, args.cpu)
    end_time = time.time()
    logger.info('Noise generation finished')
    total_time = (end_time-start_time)//60
    logger.info(f'cost {total_time} m')

    save_checkpoint(args.save_dir, '{}-fin'.format(args.save_name), model, optim, log, def_noise)

    return


if __name__ == '__main__':
    args = get_args()
    logger = utils.generic_init(args)

    logger.info('EXP: robust minimax pgd perturbation')
    try:
        main(args, logger)
    except Exception as e:
        logger.exception('Unexpected exception! %s', e)
