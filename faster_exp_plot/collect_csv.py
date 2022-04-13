
import argparse
from tensorboard.backend.event_processing import event_accumulator
import pandas as pd
import os 
from tqdm import tqdm

def export_csv(filepath:str,outputpath:str,metadata:str,savename="data.csv"):
    """
    export single csv file from single event file
    :param filepath: the path where event file locate in
    :param outputpath:
    :param metadata: which meta-data you wanna choose # currently open support scalar type
    :param savename:
    :return: None
    """
    event_data = event_accumulator.EventAccumulator(filepath)  # a python interface for loading Event data
    event_data.Reload()  # synchronously loads all of the data written so far b
    df = pd.DataFrame(event_data.Scalars(metadata))
    df.columns = ['Wall_time', 'Step', 'Value']
    df.to_csv(f'{outputpath}/{savename}', index=False)

def export_csv_from_root(rootpath:str,filepath:str,outputpath:str,metadata:str,savename="data.csv"):
    """
    recursively export csv file from event file from the root path, and save the csv file where event file located in
    :param filepath: the path where event file locate in
    :param outputpath:
    :param metadata: which meta-data you wanna choose # currently open support scalar type
    :param savename:
    :param rootpath: where to start
    :return: None
    """
    for p,d,f in tqdm(os.walk(rootpath)):
        for fi in f:
            if 'events.' in fi:
                export_csv(p,p,metadata,savename)
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument(
        '--data_dir',
        type=str,
        default='./data',
        help='The data dir where you put your tensorboard files'
    )
    args.add_argument(
        '--save_dir',
        type=str,
        default='./save_dir',
        help='The save path where you want to save export csv file'
    )
    args.add_argument(
        '--meta_data',
        type=str,
        default='mean_episode_reward/episode',
        help='Which meta data you choose to save'
    )
    args.add_argument(
        '--save_name',
        type=str,
        default='data.csv',
        help='The name of output csv file'
    )
    args.add_argument(
        '--root_dir',
        type=str,
        default='./data',
        help='The root path if you wanna export mutliple csv'
    )
    args = args.parse_args()
    # export_csv(args.data_dir,args.save_dir,args.meta_data,args.save_name)
    export_csv_from_root(args.root_dir,args.data_dir,args.save_dir,args.meta_data,args.save_name)
