# import os 
# env_list = [simple_spread, simple_tag,
#         simple_world_comm
# ]
# for i in env_list:
# #     os.system(fcd /content/drive/MyDrive/workspace/PARL/examples/MADDPG && nohup python train.py --env {i} >{i}.log 2>&1 &)
#     os.system(f"cd /ssd2/liuyixin04/workspace/PARL/examples/MADDPG  && python3 train.py --env {i}")
# pyp="/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/dl/lib:/home/work/cuda-10.0/lib64/:/home/work/cudnn_v7.4/cuda/lib64 /ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python"
# ource ~/.bashrc
# source /ssd2/liuyixin04/miniconda3/bin/activate
# conda activate py37_paddle
cd /ssd2/liuyixin04/workspace/PARL/examples/MADDPG
continous="continous"
continous_add="--continuous_actions"

for i in {1..4}
do
seed=$RANDOM 
for act_spc in continous discrete 
do
lib="/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.0/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib"
# for env in simple simple_adversary simple_crypto simple_push simple_speaker_listener simple_spread simple_tag simple_world_comm
for env in simple_tag simple_world_comm
do
# echo $env;
# cd /ssd2/liuyixin04/workspace/PARL/examples/MADDPG
# $lib  /ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python train.py --env $env --seed $seed
command="/ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python train.py --env $env --model_dir ./model-s$seed-$env-$act_spc --seed $seed"
if [ "$act_spc" = "$continous" ]
then
command="/ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python train.py --env $env --model_dir ./model-s$seed-$env-$act_spc --seed $seed $continous_add"
fi
# echo "$lib $command"
# $lib $command
echo "nohup $lib $command > log/$env-$seed-$act_spc.log 2>&1 &"
nohup $lib $command > log/$env-$seed-$act_spc.log 2>&1 &
# curl -P /ssd2/liuyixin04/workspace/PARL/examples/MADDPG/csv-out http://0.0.0.0:8081/data/plugin/scalars/scalars?tag=mean_episode_reward%2Fepisode\&run=$env\_0_False\&experiment=\&format=csv 
done;
done;
done;