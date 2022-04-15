import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import numpy as np
import pandas as pd
from pathlib import Path
import itertools
import time
from copy import deepcopy

from general_config import GeneralConfig


def csv_has_header(filename):
    with open(filename, 'r') as f:
        first_line = f.readline()
    if 'Value' in first_line:
        return True
    else:
        return False


def moving_average(x, w):
    '''
    Args:
        ndarray or list
    Returns:
        smoothed ndarray or list
    '''
    assert isinstance(x, (list, np.ndarray))
    if isinstance(x, np.ndarray):
        length = x.shape[0]
    else:
        length = len(x)
    # print(length)
    # print(w)
    assert w // 2 <= length
    result = []
    last_left = 0
    last_right = w // 2 - 1
    window_sum = np.sum(x[last_left:last_right + 1])
    for i in range(length):
        left = max(0, i - w // 2)
        right = min(length - 1, i + w // 2)  # include
        if right > last_right:
            window_sum += x[right]
        if left > last_left:
            window_sum -= x[last_left]
        count = right - left + 1
        result.append(window_sum / count)

        last_left = left
        last_right = right

    if isinstance(x, np.ndarray):
        return np.array(result, dtype='float32')
    else:
        return result


def get_single_csv_data(csv_filename):
    
    has_header = csv_has_header(csv_filename)
    if has_header:
        df = pd.read_csv(csv_filename, sep=',')
    else:
        df = pd.read_csv(
            csv_filename,
            header=None,
            # names=['time', 'train_step', 'Step', 'Value'],
            names=['time', 'Step', 'Value'],
            sep=',')
    return df


def get_smoothed_csv_data(csv_filename, point_interval, reference_window_size, window_size_increase_rate):
    ''' Sample smoothed points according to the interval
    Args:
        csv_filename: csv file
        smoothing_window_size: window size to do a moving average.
    Returns:
        Steps (list): smoothed step
        value (list): smoothed value
    '''

    has_header = csv_has_header(csv_filename)
    if has_header:
        df = pd.read_csv(csv_filename, sep=',')
    else:
        df = pd.read_csv(
            csv_filename,
            header=None,
            names=['time', 'train_step', 'Step', 'Value'],
            sep=',')
    # print('origin df shape : {}'.format(df.shape))
    df['Step'] = (df['Step'].values // point_interval * point_interval).astype('int64')
    new_df = df.groupby('Step').mean()
    # print('new_df.shape:{}'.format(new_df.shape))

    steps = new_df.index.values.astype('int64').tolist()
    values = new_df['Value'].values.tolist()
    point_dense = len(steps) / steps[-1]
    relative_point_dense = point_dense * 1000 * window_size_increase_rate
    smoothing_window_size = int(relative_point_dense * reference_window_size)
    print('window_size: {}'.format(smoothing_window_size))
    smoothed_values = moving_average(values, smoothing_window_size)
    # smoothed_values = values
    return steps, smoothed_values


def calc_mean_and_confidence(csv_file_list,
                             reference_window_size, window_size_increase_rate):
    print('num experients: {}'.format(len(csv_file_list)))
    steps_all = []
    values_all = []

    first_df = get_single_csv_data(csv_file_list[0])
    # print(first_df)
    first_steps = first_df['Step'].values
    # print(first_steps)
    point_interval = first_steps[-1] // first_steps.shape[0]

    for csv_file_name in csv_file_list:
        steps, values = get_smoothed_csv_data(csv_file_name, point_interval,
                                              reference_window_size, window_size_increase_rate)
        steps_all.append(steps)
        values_all.append(values)
        print('len steps : {}, values {}'.format(len(steps), len(values)))
    # print(steps,values)
    # print('debug')
    # make sure that all csv files has the same steps
    selected_steps = []
    selected_values = [[] for _ in range(len(steps_all))]
    while True:
        if np.any([len(steps) == 0 for steps in steps_all]):
            break
        max_step = np.max([steps[0] for steps in steps_all])
        select = True
        for i in range(len(steps_all)):
            if steps_all[i][0] < max_step:
                steps_all[i].pop(0)
                values_all[i].pop(0)
                select = False
        if select == True:
            selected_steps.append(max_step)
            for i in range(len(steps_all)):
                selected_values[i].append(values_all[i][0])
                steps_all[i].pop(0)
                values_all[i].pop(0)

    std = []
    for i in range(len(selected_values[0])):
        std.append(np.std([values[i] for values in selected_values]))
    assert len(std) == len(selected_steps)
    std = np.array(std)

    selected_values_all = np.array(selected_values)
    values_mean = np.mean(selected_values_all, axis=0)
    values_ub = values_mean + std
    values_lb = values_mean - std
    selected_steps = np.array(selected_steps)

    print('steps: {}, mean: {}, ub: {}, lb: {}'.format(
        selected_steps.shape, values_mean.shape, values_ub.shape,
        values_lb.shape))
    return selected_steps, values_mean, values_ub, values_lb


def plot_mean_and_CI(ax,
                     x,
                     mean,
                     ub,
                     lb,
                     color_mean=None,
                     color_shading=None,
                     line=None,
                     alg=None):
    ax.fill_between(x, ub, lb, color=color_shading, alpha=0.2, lw=0.0)
    line = ax.plot(x, mean, color=color_mean, lw=1,label=alg)


def draw_single_env(all_csv_file_list, ax, task_config, env_config, max_step,end):
    for i in range(len(task_config['algorithms'])):
        print(task_config['algorithms'][i])
        x, mean, ub, lb = calc_mean_and_confidence(
            all_csv_file_list[i], task_config['reference_window_size'], task_config['window_size_increase_rate'])
        plot_mean_and_CI(
            ax,
            x,
            mean,
            ub,
            lb,
            color_mean=env_config['pic_color'][i],
            color_shading=env_config['pic_color'][i],
            line=None,
            alg=task_config['line_labels'][i])

    ax.set_title(env_config['fig_title'], fontsize=10)  # override title size
    # ax.set_xlabel(env_config['x_label'], fontsize=7)
    # ax.set_ylabel(env_config['y_label'], fontsize=9)

    ax.set_xlim(0, max_step)
    ax.set_ylim(env_config['min_y'], env_config['max_y'])

    xmajorLocator = tick.MultipleLocator(env_config['x_major_loc'])
    ymajorLocator = tick.MultipleLocator(env_config['y_major_loc'])
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.tick_params(labelsize=8)

    # xminorLocator = tick.MultipleLocator(env_config['x_minor_loc'])
    # yminorLocator = tick.MultipleLocator(env_config['y_minor_loc'])
    # ax.xaxis.set_minor_locator(xminorLocator)
    # ax.yaxis.set_minor_locator(yminorLocator)
    ax.grid(alpha=0.3)  # add grid lines
    
    # legend
    # if end:
    #     ax.legend(loc="lower right")


def get_all_csv_filename(path):
    result = list(
        map(lambda x: str(x.resolve()),
            list(Path(path).rglob("*.[c][s][v]"))))
    return result


def main(task_config, general_config):
    path = task_config['root_path']
    all_csv_files = get_all_csv_filename(path)
    print(all_csv_files)
    fig, axs = plt.subplots(task_config['subplot'][0], task_config['subplot'][1])
    if task_config['subplot'][0] == 1:
        axs = axs.reshape([1, -1])
    if task_config['subplot'][1] == 1:
        axs = axs.reshape([-1, 1])

        # __import__('pdb').set_trace()
    axes = list(itertools.chain.from_iterable(axs))
    print(len(axes))
    print(axes[-1])
    print(type(axes[-1]))
    # axes[-1].remove()
    print(len(axes))
    print(axes)
    for i, env in enumerate(task_config['envs']):
        print('-----------env: {} -----------'.format(env))
        all_algs_files = []
        for alg_name in task_config['algorithms']:
            f = list(
                    filter(lambda x: alg_name + '/' + env +'/' in x,
                           all_csv_files))
            # print('过滤')
            # print(f)
            all_algs_files.append(f)
        print(len(axes))
        print(len(task_config['env_steps']))
        print(i)
        
        draw_single_env(all_algs_files, axes[i], task_config,
                        general_config[env], task_config['env_steps'][i],end=(i==(len(task_config['envs'])-1)))
        # leg = fig.legend(
        #     labels=task_config['line_labels'],
        #     bbox_to_anchor=(0.85, 0.08),
        #     loc='lower right',
        #     frameon=False)
    fig.tight_layout(pad=0.4)
    # for legobj in leg.legendHandles:
    #     legobj.set_linewidth(4.0)
    # TODO: 删除空白的子图
    plt.delaxes()
    plt.savefig(task_config['output_name'], dpi=300)
    # plt.show()


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',type=str,default='/ssd2/liuyixin04/workspace/PARL/examples/MADDPG/plot_dir')
    parser.add_argument('--output',type=str,default='./result.png')
    args = parser.parse_args()

    start_time = time.time()
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 8  # set global global font size
    plt.rcParams["figure.figsize"] = (12, 6.75)  # set global fig size
    general_config = deepcopy(GeneralConfig)
    # legend, minor axis, xlabel and ylabel functions are disabled to produce this template.

    # mujoco_task_config = {
    #     'subplot': (3, 3),
    #     'root_path': './ijcai_result',
    #     'algorithms': ['EAC', 'TD3', 'DDPG', 'PPO', 'SAC'],
    #     'envs': [
    #         'HalfCheetah-v1', 'Hopper-v1', 'Walker2d-v1', 'Swimmer-v1',
    #         'Humanoid-v1', 'BipedalWalkerHardcore-v2', 'RoboschoolHumanoid-v1',
    #         'RoboschoolHumanoidFlagrun-v1'
    #     ],
    #     'line_labels': ['EAC', 'TD3', 'DDPG', 'PPO', 'SAC'],
    #     'reference_window_size': 3,
    #     'window_size_increase_rate': 60,
    #     'env_steps': [5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000, 5000000],
    #     'output_name': 'result.pdf'
    # }

    # args.output
    task_config = {
        'subplot': (3, 3),
        'root_path': args.path,
        'algorithms': ['MADDPG-continous','MADDPG-discrete'],
        'envs': [
                'simple', 'simple_adversary', 'simple_crypto', 'simple_push',
                'simple_speaker_listener', 'simple_spread', 'simple_tag',
                'simple_world_comm'
            ],
        'line_labels': ['continous','discrete'],
        'reference_window_size': 2,
        'window_size_increase_rate': 1,
        'env_steps': [25000]*5+[100000]*3,
        'output_name': args.output
    }
    main(task_config, general_config)
    print('finished! total time: {} s'.format(time.time() - start_time))
