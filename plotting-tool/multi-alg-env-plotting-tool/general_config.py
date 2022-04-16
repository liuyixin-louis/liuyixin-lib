import copy

GeneralConfig = {}
GeneralConfig['HalfCheetah-v1']= {
  'min_y': 0,          # Y轴最小值
  'max_y': 11000,      # Y轴最大值
  'has_header': False,  #csv文件第一行不是header，那就需要用数字指明col_to_x和col_to_y是第几列的数据
  'col_to_x': 2, # csv文件中对应的列作为x坐标
  'col_to_y': 3,
  'x_label': 'Environment Steps', # X轴标题
  'y_label': 'Score',       # Y轴标题
  'x_major_loc': 1000000,  # x轴主刻度
  'y_major_loc': 5000,     # y轴主刻度
  'x_minor_loc': 200000,    # x轴副刻度
  'y_minor_loc': 1000,     # y轴副刻度
  'pic_color': ['#e41b1d', '#377eb8', '#50b04d', '#c435cc', '#f08536', '#85584e'],
  'pic_width': 7,
  'pic_height': 4,
}

GeneralConfig['BreakoutNoFrameskip-v4'] = {
  'min_y': 0,          # Y轴最小值
  'max_y': 500,      # Y轴最大值
  'has_header': True,  #csv文件第一行不是header，那就需要用数字指明col_to_x和col_to_y是第几列的数据
  'col_to_x': 1, # csv文件中对应的列作为x坐标
  'col_to_y': 2,
  'x_major_loc': 2000000,  # x轴主刻度
  'y_major_loc': 100,     # y轴主刻度
  'pic_color': ['#e41b1d', '#377eb8', '#50b04d', '#c435cc', '#f08536', '#85584e'],
}

# Hopper-v1
GeneralConfig['Hopper-v1'] = copy.deepcopy(GeneralConfig['HalfCheetah-v1'])
GeneralConfig['Hopper-v1']['max_y'] = 4000
GeneralConfig['Hopper-v1']['y_major_loc'] = 1000
GeneralConfig['Hopper-v1']['y_minor_loc'] = 200

# Walker2d-v1
GeneralConfig['Walker2d-v1'] = copy.deepcopy(GeneralConfig['HalfCheetah-v1'])
GeneralConfig['Walker2d-v1']['max_y'] = 5500
GeneralConfig['Walker2d-v1']['y_major_loc'] = 1000
GeneralConfig['Walker2d-v1']['y_minor_loc'] = 200

# Swimmer-v1
GeneralConfig['Swimmer-v1'] = copy.deepcopy(GeneralConfig['HalfCheetah-v1'])
GeneralConfig['Swimmer-v1']['max_y'] = 200
GeneralConfig['Swimmer-v1']['y_major_loc'] = 100
GeneralConfig['Swimmer-v1']['y_minor_loc'] = 20

# Humanoid-v1
GeneralConfig['Humanoid-v1'] = copy.deepcopy(GeneralConfig['HalfCheetah-v1'])
GeneralConfig['Humanoid-v1']['max_y'] = 5500
GeneralConfig['Humanoid-v1']['min_y'] = -500
GeneralConfig['Humanoid-v1']['y_major_loc'] = 2000
GeneralConfig['Humanoid-v1']['y_minor_loc'] = 400

# BipedalWalkerHardcore-v2
GeneralConfig['BipedalWalkerHardcore-v2'] = copy.deepcopy(GeneralConfig['HalfCheetah-v1'])
GeneralConfig['BipedalWalkerHardcore-v2']['max_y'] = 40
GeneralConfig['BipedalWalkerHardcore-v2']['min_y'] = -150
GeneralConfig['BipedalWalkerHardcore-v2']['y_major_loc'] = 100
GeneralConfig['BipedalWalkerHardcore-v2']['y_minor_loc'] = 20

# RoboschoolHumanoidFlagrun-v1
GeneralConfig['RoboschoolHumanoidFlagrun-v1'] = copy.deepcopy(GeneralConfig['HalfCheetah-v1'])
GeneralConfig['RoboschoolHumanoidFlagrun-v1']['min_y'] = -700
GeneralConfig['RoboschoolHumanoidFlagrun-v1']['max_y'] = 1500
GeneralConfig['RoboschoolHumanoidFlagrun-v1']['y_major_loc'] = 1000
GeneralConfig['RoboschoolHumanoidFlagrun-v1']['y_minor_loc'] = 200

GeneralConfig['RoboschoolHumanoid-v1'] = copy.deepcopy(GeneralConfig['HalfCheetah-v1'])
GeneralConfig['RoboschoolHumanoid-v1']['min_y'] = -900
GeneralConfig['RoboschoolHumanoid-v1']['max_y'] = 1600
GeneralConfig['RoboschoolHumanoid-v1']['y_major_loc'] = 1000
GeneralConfig['RoboschoolHumanoid-v1']['y_minor_loc'] = 200

GeneralConfig['PongNoFrameskip-v4'] = copy.deepcopy(GeneralConfig['BreakoutNoFrameskip-v4'])
GeneralConfig['PongNoFrameskip-v4']['max_y'] = 25
GeneralConfig['PongNoFrameskip-v4']['min_y'] = -25
GeneralConfig['PongNoFrameskip-v4']['y_major_loc'] = 10

GeneralConfig['simple']= {
  'min_y': -40,          # Y轴最小值
  'max_y': 0,      # Y轴最大值
  'has_header': True,  #csv文件第一行不是header，那就需要用数字指明col_to_x和col_to_y是第几列的数据
  'x_label': 'Environment Steps', # X轴标题
  'y_label': 'Score',       # Y轴标题
  'x_major_loc': 5000,  # x轴主刻度
  'y_major_loc': 10,     # y轴主刻度
  'x_minor_loc': 10000,    # x轴副刻度
  'y_minor_loc': 10000,     # y轴副刻度
  'pic_color': ['#e41b1d', '#377eb8'],
  'pic_width': 7,
  'pic_height': 4,
}

#  '#50b04d', '#c435cc', '#f08536', '#85584e'

GeneralConfig['simple_adversary'] = copy.deepcopy(GeneralConfig['simple'])
GeneralConfig['simple_adversary']['max_y'] = 10
GeneralConfig['simple_adversary']['min_y'] = -20
GeneralConfig['simple_adversary']['y_major_loc'] = 10

GeneralConfig['simple_push'] = copy.deepcopy(GeneralConfig['simple'])
GeneralConfig['simple_push']['max_y'] = 0
GeneralConfig['simple_push']['min_y'] = -30
GeneralConfig['simple_push']['y_major_loc'] = 10

GeneralConfig['simple_crypto'] = copy.deepcopy(GeneralConfig['simple'])
GeneralConfig['simple_crypto']['max_y'] = 30
GeneralConfig['simple_crypto']['min_y'] = -40
GeneralConfig['simple_crypto']['y_major_loc'] = 5

GeneralConfig['simple_speaker_listener'] = copy.deepcopy(GeneralConfig['simple'])
GeneralConfig['simple_speaker_listener']['max_y'] = 0
GeneralConfig['simple_speaker_listener']['min_y'] = -100
GeneralConfig['simple_speaker_listener']['y_major_loc'] = 50

GeneralConfig['simple_spread'] = copy.deepcopy(GeneralConfig['simple'])
GeneralConfig['simple_spread']['max_y'] = -48
GeneralConfig['simple_spread']['min_y'] = -188
GeneralConfig['simple_spread']['y_major_loc'] = 5
GeneralConfig['simple_spread']['x_major_loc'] = 20000


GeneralConfig['simple_tag'] = copy.deepcopy(GeneralConfig['simple'])
GeneralConfig['simple_tag']['max_y'] = 117.18
GeneralConfig['simple_tag']['min_y'] = -12.42
GeneralConfig['simple_tag']['y_major_loc'] = 20
GeneralConfig['simple_tag']['x_major_loc'] = 20000


GeneralConfig['simple_world_comm'] = copy.deepcopy(GeneralConfig['simple'])
GeneralConfig['simple_world_comm']['max_y'] = 48.84
GeneralConfig['simple_world_comm']['min_y'] =  -77.28
GeneralConfig['simple_world_comm']['y_major_loc'] = 20
GeneralConfig['simple_world_comm']['x_major_loc'] = 20000

config_from_statis = {'simple_adversary': {'max_y': 0,
  'min_y': -20,
  'mean_endy': -3.622999995946884,
  'y_major_loc': 5},
 'simple': {'max_y': 0,
  'min_y': -40,
  'mean_endy': -5.476857117244175,
  'y_major_loc': 10},
 'simple_tag': {'max_y': 60,
  'min_y': -20,
  'mean_endy': 5.078749895095825,
  'y_major_loc': 20},
 'simple_world_comm': {'max_y': 60,
  'min_y': -60,
  'mean_endy': 25.607500076293945,
  'y_major_loc': 30},
 'simple_spread': {'max_y': -40,
  'min_y': -200,
  'mean_endy': -102.2490005493164,
  'y_major_loc': 40},
 'simple_speaker_listener': {'max_y': 0,
  'min_y': -100,
  'mean_endy': -24.63675022125244,
  'y_major_loc': 25},
 'simple_push': {'max_y': 0,
  'min_y': -40,
  'mean_endy': -7.73800003528595,
  'y_major_loc': 10},
 'simple_crypto': {'max_y': 20,
  'min_y': -40,
  'mean_endy': -9.475874841213226,
  'y_major_loc': 15}}




for k,v in config_from_statis.items():
  GeneralConfig[k]['max_y'] = v["max_y"]
  GeneralConfig[k]['min_y'] = v["min_y"]
  GeneralConfig[k]['y_major_loc'] = v["y_major_loc"]


for env, env_config in GeneralConfig.items():
    env_config['fig_title'] = env
    env_config['pic_filename'] = env + '.png'