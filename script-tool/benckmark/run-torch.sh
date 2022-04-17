cd /ssd2/liuyixin04/workspace/my-parl/PARL/benchmark/torch/maddpg
continous="continous"
continous_add="--continuous_actions"
experiment_name="benchmark-torch-continous-extra"
logdir="/ssd2/liuyixin04/workspace/logs/$experiment_name/"
py="/ssd2/liuyixin04/miniconda3/envs/py37_torch/bin/python"
pyfile="train.py"
rm -r $logdir
mkdir $logdir
modeldir=$logdir/"model"
mkdir $modeldir
export PARL_BACKEND="torch"
mkdir $logdir/back_logs
trainlog=$logdir/"train_log/"

i=0 # gpu pointer
gpu=(1 2 3 4 5 6 7)
for i in {1..4}
do
seed=$RANDOM 
for act_spc in continous 
do
lib="/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.0/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib"
# for env in simple simple_adversary simple_crypto simple_push simple_speaker_listener simple_spread simple_tag simple_world_comm
# for env in simple_spread
for env in simple_spread simple_tag simple_world_comm
do
command="$py $pyfile --env $env --model_dir $modeldir/s$seed-$env-$act_spc --seed $seed --log_dir $trainlog"
if [ "$act_spc" = "$continous" ]
then
command=$command" $continous_add"
fi
## gpu
i=`expr $i % 7`
export CUDA_VISIBLE_DEVICES=${gpu[$i]}
# echo ${gpu[$i]}
i=`expr $i + 1`
###
# echo "$lib $command"
# $lib $command
echo "nohup $lib $command > $logdir/back_logs/$env-$seed-$act_spc.log 2>&1 &"
nohup $lib $command > $logdir/back_logs/$env-$seed-$act_spc.log 2>&1 &
done;
done;
done;