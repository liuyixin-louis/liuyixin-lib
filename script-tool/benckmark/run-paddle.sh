cd /ssd2/liuyixin04/workspace/my-parl/PARL/examples/MADDPG/
continous="continous"
continous_add="--continuous_actions"
experiment_name="benchmark-paddle"
logdir="/ssd2/liuyixin04/workspace/logs/$experiment_name"
py="/ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python"
pyfile="train.py"
mkdir $logdir
modeldir=$logdir/"model"
mkdir $modeldir
export PARL_BACKEND="paddle"
mkdir $logdir/back_logs

for i in {1..4}
do
seed=$RANDOM 
for act_spc in continous discrete 
do
lib="/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.0/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib"
for env in simple simple_adversary simple_crypto simple_push simple_speaker_listener simple_spread simple_tag simple_world_comm
# for env in simple_spread
do
# echo $env;
# cd /ssd2/liuyixin04/workspace/PARL/examples/MADDPG
# $lib  /ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python train.py --env $env --seed $seed
command="$py $pyfile --env $env --model_dir $modeldir/s$seed-$env-$act_spc --seed $seed"
if [ "$act_spc" = "$continous" ]
then
command="$py $pyfile --env $env --model_dir $modeldir/s$seed-$env-$act_spc --seed $seed $continous_add"
fi
# echo "$lib $command"
# $lib $command
echo "nohup $lib $command > $logdir/back_logs/$env-$seed-$act_spc.log 2>&1 &"
nohup $lib $command > $logdir/back_logs/$env-$seed-$act_spc.log 2>&1 &
# curl -P /ssd2/liuyixin04/workspace/PARL/examples/MADDPG/csv-out http://0.0.0.0:8081/data/plugin/scalars/scalars?tag=mean_episode_reward%2Fepisode\&run=$env\_0_False\&experiment=\&format=csv 
done;
done;
done;