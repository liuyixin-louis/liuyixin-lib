root=/ssd2/liuyixin04/workspace/my-repo-yixin/robust_noise
cd $root
lib="/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.0/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib"
pyt="/ssd2/liuyixin04/miniconda3/envs/py37_torch/bin/python"
noise_train_step=10000
expname="double-uniform-random-attack"

$lib $pyt generate_robust_em_random_pertub.py \
    --arch resnet18 \
    --dataset cifar10 \
    --train-steps $noise_train_step \
    --batch-size 8 \
    --optim sgd \
    --lr 0.1 \
    --lr-decay-rate 0.1 \
    --lr-decay-freq 2000 \
    --weight-decay 5e-4 \
    --momentum 0.9 \
    --pgd-radius 8 \
    --pgd-steps 10 \
    --pgd-step-size 1.6 \
    --pgd-random-start \
    --atk-pgd-radius 4 \
    --atk-pgd-steps 10 \
    --atk-pgd-step-size 0.8 \
    --atk-pgd-random-start \
    --samp-num 5 \
    --report-freq 1000 \
    --save-freq 1000 \
    --data-dir ~/dataset/ \
    --save-dir ./exp_data/cifar10/$expname-random-pertub-noise-$noise_train_step/rem8-4 \
    --save-name random_attack

$lib $pyt train.py \
    --arch resnet18 \
    --dataset cifar10 \
    --train-steps 40000 \
    --batch-size 8 \
    --optim sgd \
    --lr 0.1 \
    --lr-decay-rate 0.1 \
    --lr-decay-freq 16000 \
    --weight-decay 5e-4 \
    --momentum 0.9 \
    --pgd-radius 4 \
    --pgd-steps 10 \
    --pgd-step-size 0.8 \
    --pgd-random-start \
    --report-freq 1000 \
    --save-freq 100000 \
    --noise-path ./exp_data/cifar10/$expname-random-pertub-noise-$noise_train_step/rem8-4/random_attack-fin-def-noise.pkl \
    --data-dir ~/dataset/ \
    --save-dir ./exp_data/cifar10/$expname-random-pertub/rem8-4/r4 \
    --save-name random_attack_train
