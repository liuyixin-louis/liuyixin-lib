from PIL import Image
import numpy as np
import torch
import torchvision
import os
import pickle
# from torchvision import datasets
# from torchvision import transforms
# import torchsample.transforms as tstf


class ElementWiseTransform():
    def __init__(self, trans=None):
        self.trans = trans

    def __call__(self, x):
        if self.trans is None: return x
        return torch.cat( [self.trans( xx.view(1, *xx.shape) ) for xx in x] )


class IndexedTensorDataset():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, idx):
        x, y = self.x[idx], self.y[idx]
        ''' transform HWC pic to CWH pic '''
        # x = torch.tensor(x, dtype=torch.float32).permute(2,0,1)
        x = torch.tensor(x, dtype=torch.float32)
        return x, y, idx

    def __len__(self):
        return len(self.x)


class Dataset():
    def __init__(self, x, y, transform=None, fitr=None):
        self.x = x
        self.y = y
        self.transform = transform
        self.fitr = fitr

    def __getitem__(self, idx):
        x, y = self.x[idx], self.y[idx]

        ''' low pass filtering '''
        if self.fitr is not None:
            x = self.fitr(x)

        ''' data augmentation '''
        if self.transform is not None:
            # if x.shape[0] == 1:
            #     print("asda")
            #     x = np.squeeze(x, axis=2)
            # print(x.shape)
            x = Image.fromarray(x)
            x = self.transform(x)
        

        return x, y

    def __len__(self):
        return len(self.x)


class IndexedDataset():
    def __init__(self, x, y, transform=None):
        self.x = x
        self.y = y
        self.ii = np.array( range(len(x)), dtype=np.int64 )
        self.transform = transform

    def __getitem__(self, idx):
        x, y, ii = Image.fromarray(self.x[idx]), self.y[idx], self.ii[idx]
        if self.transform is not None:
            x = self.transform(x)
        return x, y, ii

    def __len__(self):
        return len(self.x)


def datasetMNIST(root='./path', train=True, transform=None):
    return torchvision.datasets.MNIST(root=root, train=train,
                        transform=transform, download=True)

def datasetSVHN(root='./path', train=True, transform=None):
    return torchvision.datasets.SVHN(root=root, split="train" if train else "test",
                        transform=transform, download=True)

def datasetCIFAR10(root='./path', train=True, transform=None):
    return torchvision.datasets.CIFAR10(root=root, train=train,
                        transform=transform, download=True)

def datasetCIFAR100(root='./path', train=True, transform=None):
    return torchvision.datasets.CIFAR100(root=root, train=train,
                        transform=transform, download=True)

def datasetTinyImageNet(root='./path', train=True, transform=None):
    if train: root = os.path.join(root, 'tiny-imagenet_train.pkl')
    else: root = os.path.join(root, 'tiny-imagenet_val.pkl')
    with open(root, 'rb') as f:
        dat = pickle.load(f)
    return Dataset(dat['data'], dat['targets'], transform)
    # root = os.path.join(root, 'tiny-imagenet-200')
    # if train: root = os.path.join(root, 'train')
    # else: root = os.path.join(root, 'val', 'images')
    # raw_dataset = torchvision.datasets.ImageFolder(root)
    # xx, yy = [], []
    # for i in range( len(raw_dataset) ):
    #     x, y = raw_dataset[i]
    #     x = np.array(x)
    #     xx.append( x.reshape(1, *x.shape) )
    #     yy.append( y )
    # xx = np.concatenate(xx)
    # yy = np.array(yy)

    # dat = {'data':xx, 'targets':yy}
    # if train: save_name = 'tiny-imagenet_train.pkl'
    # else: save_name = 'tiny-imagenet_val.pkl'

    # import pickle
    # with open('./data/{}'.format(save_name), 'wb') as f:
    #     pickle.dump(dat, f)
    # exit()
    # return Dataset(xx, yy, transform)

#
# def prepare_imagenet(args):
#     dataset_dir = os.path.join(args.data_dir, args.dataset)
#     train_dir = os.path.join(dataset_dir, 'train')
#     val_dir = os.path.join(dataset_dir, 'val', 'images')
#     kwargs = {} if args.no_cuda else {'num_workers': 1, 'pin_memory': True}
#
#     # Pre-calculated mean & std on imagenet:
#     # norm = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
#     # For other datasets, we could just simply use 0.5:
#     # norm = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
#
#     print('Preparing dataset ...')
#     # Normalization
#     norm = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) \
#         if args.pretrained else transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
#
#     # Normal transformation
#     if args.pretrained:
#         train_trans = [transforms.RandomHorizontalFlip(), transforms.RandomResizedCrop(224),
#                        transforms.ToTensor()]
#         val_trans = [transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), norm]
#     else:
#         train_trans = [transforms.RandomHorizontalFlip(), transforms.ToTensor()]
#         val_trans = [transforms.ToTensor(), norm]
#
#     # Data augmentation (torchsample)
#     # torchsample doesn't really help tho...
#     if args.ts:
#         train_trans += [tstf.Gamma(0.7),
#                         tstf.Brightness(0.2),
#                         tstf.Saturation(0.2)]
#
#     train_data = datasets.ImageFolder(train_dir,
#                                       transform=transforms.Compose(train_trans + [norm]))
#
#     val_data = datasets.ImageFolder(val_dir,
#                                     transform=transforms.Compose(val_trans))
#
#     print('Preparing data loaders ...')
#     train_data_loader = torch.utils.data.DataLoader(train_data, batch_size=args.batch_size,
#                                                     shuffle=True, **kwargs)
#
#     val_data_loader = torch.utils.data.DataLoader(val_data, batch_size=args.test_batch_size,
#                                                   shuffle=True, **kwargs)
#
#     return train_data_loader, val_data_loader, train_data, val_data

class Loader():
    def __init__(self, dataset, batch_size, shuffle=False, drop_last=False, num_workers=4,parallel=False):
        # if parallel:
        #     self.sampler = torch.utils.data.distributed.DistributedSampler(dataset)
        #     self.loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, \
        #         drop_last=drop_last, sampler=self.sampler,pin_memory=False)
        # else:
        self.loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, \
            drop_last=drop_last, num_workers=num_workers)
        self.iterator = None

    def __iter__(self):
        return iter(self.loader)

    def __len__(self):
        return len(self.loader)

    def __next__(self):
        if self.iterator is None:
            self.iterator = iter(self.loader)

        try:
            samples = next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.loader)
            samples = next(self.iterator)

        return samples
