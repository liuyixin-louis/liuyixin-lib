root="/mnt/yixin/liuyixin-lib/project/robust_noise"
cd $root
source activate py38
export CUDA_VISIBLE_DEVICES=0
python train.py \
    --arch resnet18 \
    --dataset mnist-extreme \
    --train-steps 800 \
    --batch-size 128 \
    --optim sgd \
    --lr 0.1 \
    --lr-decay-rate 0.1 \
    --lr-decay-freq 400 \
    --weight-decay 5e-4 \
    --momentum 0.9 \
    --pgd-radius 4 \
    --pgd-steps 10 \
    --pgd-step-size 0.8 \
    --pgd-random-start \
    --report-freq 100 \
    --save-freq 100000 \
    --noise-path ./exp_data/mnist-extreme/noise-test/rem8-4/rem-fin-def-noise.pkl \
    --data-dir ./data \
    --save-dir ./exp_data/train/mnist-extreme/rem8-4/r4 \
    --save-name train
