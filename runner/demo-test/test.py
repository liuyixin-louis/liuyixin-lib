import argparse

from pip import main

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    
    args.add_argument('--model',type=str,default='resnet-18')
    args.add_argument('--seed',type=int,default=8)
    args.add_argument('--method',type=str,default='old')
    args.add_argument('--long_epoch',action="store_true")
    args = args.parse_args()
    
    print('testing')
    print(args.model)
    print(args.seed)
    print(args.method)
    print(args.long_epoch)
    