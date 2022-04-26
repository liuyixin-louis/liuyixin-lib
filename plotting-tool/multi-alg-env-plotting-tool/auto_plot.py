
id = "paddle"
output = f"./result-{id}.png"
trian_logdir = f"./benchmark-{id}/train_log"

from tensorboard.backend.event_processing import event_accumulator
import argparse
import pandas as pd
from tqdm import tqdm
import os 
import time

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

g = os.walk(trian_logdir)
ckpt = []
for path, dir_list, file_names in g:
    # print(path,dir_name,file_names)
    for dir_name in dir_list:
        # print()
        sub_path = os.path.join(path, dir_name)
        ckpt.append(sub_path)
        # break
    # break
    # for f in file_names:
    #     ckpt.append(os.path.join(path,f))

# ckpt=[f for f in ckpt if 'event' in f ]
# in_path='/ssd2/liuyixin04/workspace/PARL/examples/MADDPG/train_log/simple_3013_False'
for in_path in tqdm(ckpt):
    print(input)
    event_data = event_accumulator.EventAccumulator(in_path)  # a python interface for loading Event data
    event_data.Reload()  # synchronously loads all of the data written so far b
    df = pd.DataFrame(event_data.Scalars('mean_episode_reward/episode'))
    df.columns = ['Wall_time', 'Step', 'Value']
    df.to_csv(f'{in_path}/data.csv',index=False)
    print(in_path)
    # break

# create dir
root = f'/ssd2/liuyixin04/workspace/logs/tmp/{id}-tmp-{time.time()}'
mkdir(root)
algs = ['MADDPG-continous','MADDPG-discrete']
for alg in algs:
    mkdir(os.path.join(root,alg))
envs = [
        'simple', 'simple_adversary', 'simple_crypto', 'simple_push',
        'simple_speaker_listener', 'simple_spread', 'simple_tag',
        'simple_world_comm'
    ]
for alg in algs:
    for env in envs:
        path=os.path.join(root,alg)
        mkdir(os.path.join(path,env))
datalist = [f+'/data.csv' for f in ckpt]
flaglist = [d.split('/')[-2] for d in datalist]
flaglist
for i,csv in enumerate(datalist):
    path = root
    if 'True' in flaglist[i]:
        path=os.path.join(path,'MADDPG-continous')
    else:
        path=os.path.join(path,'MADDPG-discrete')
    path = os.path.join(path,'_'.join(flaglist[i].split('_')[:-2]))
    # '/'.join(csv.split('/')[:-1])
    csv_old = os.path.join(path,'data.csv')
    csv_new = csv_old.replace('data','_'.join(flaglist[i].split('_')[-2:]))
    # os.system(f"rm {csv_old}")
    os.system(f'cp {csv} {path}')
    os.system(f"mv {csv_old} {csv_new}")
os.system(f'/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.0/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib /ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python /ssd2/liuyixin04/workspace/my-repo-yixin/auto-plot-yixin/result-drawing-master/draw_benchmark.py --path {root} --output {output}')