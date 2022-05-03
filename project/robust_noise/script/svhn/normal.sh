cd $(dirname $(dirname $(dirname "$0")))
source activate py38
export CUDA_VISIBLE_DEVICES=0
train_epoch=15
training_sample=50000
batch_size=128
exp_name="svhn"
noise_name="baseline"
attack_r=4
protect_r=8

noise_train_step=$(((train_epoch*training_sample)/batch_size))
down_lr_step=$((noise_train_step/2))
report_step=$((noise_train_step/2))
train_eval_step=$((noise_train_step*2))
train_eval_lr_decay_step=$((train_eval_step/2))
report_step_eval=$((train_eval_step/2))

python generate_rem.py \
    --arch resnet18 \
    --dataset $exp_name \
    --train-steps $noise_train_step \
    --batch-size $batch_size \
    --optim sgd \
    --lr 0.1 \
    --lr-decay-rate 0.1 \
    --lr-decay-freq $down_lr_step \
    --weight-decay 5e-4 \
    --momentum 0.9 \
    --pgd-radius $protect_r \
    --pgd-steps 10 \
    --pgd-step-size 1.6 \
    --pgd-random-start \
    --atk-pgd-radius $attack_r \
    --atk-pgd-steps 10 \
    --atk-pgd-step-size 0.8 \
    --atk-pgd-random-start \
    --samp-num 5 \
    --report-freq $report_step \
    --save-freq 100000 \
    --data-dir ./data \
    --save-dir ./exp_data/$exp_name/$noise_name-noise/$protect_r-$attack_r \
    --save-name $noise_name

python train.py \
    --arch resnet18 \
    --dataset $exp_name \
    --train-steps $train_eval_step \
    --batch-size $batch_size \
    --optim sgd \
    --lr 0.1 \
    --lr-decay-rate 0.1 \
    --lr-decay-freq $train_eval_lr_decay_step \
    --weight-decay 5e-4 \
    --momentum 0.9 \
    --pgd-radius $attack_r \
    --pgd-steps 10 \
    --pgd-step-size 0.8 \
    --pgd-random-start \
    --report-freq $report_step_eval \
    --save-freq 100000 \
    --noise-path ./exp_data/$exp_name/$noise_name-noise/$protect_r-$attack_r/$noise_name-fin-def-noise.pkl \
    --data-dir ./data \
    --save-dir ./exp_data/train/$exp_name/rem$protect_r-$attack_r/ \
    --save-name train
