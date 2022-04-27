source /ssd2/liuyixin04/start.sh
root="/ssd2/liuyixin04/workspace/yixin-library/project/robust_noise"
cd $root
lib="/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.2/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib"
pyt="/ssd2/liuyixin04/miniconda3/envs/py37_torch/bin/python"
export CUDA_VISIBLE_DEVICES=1

$lib $pyt train.py \
    --arch resnet18 \
    --dataset mnist-mini \
    --train-steps 5600 \
    --batch-size 128 \
    --optim sgd \
    --lr 0.1 \
    --lr-decay-rate 0.1 \
    --lr-decay-freq 2240 \
    --weight-decay 5e-4 \
    --momentum 0.9 \
    --pgd-radius 4 \
    --pgd-steps 10 \
    --pgd-step-size 0.8 \
    --pgd-random-start \
    --report-freq 1000 \
    --save-freq 100000 \
    --noise-path ./exp_data/mnist/noise-test/rem8-4/rem-fin-def-noise.pkl \
    --data-dir ./data \
    --save-dir ./exp_data/train/mnist-mini-baseline/rem8-4/r4 \
    --save-name train
