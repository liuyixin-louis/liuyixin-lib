source /ssd2/liuyixin04/start.sh
root="/ssd2/liuyixin04/workspace/yixin-library/project/robust_noise"
cd $root
lib="/opt/compiler/gcc-10/lib/ld-linux-x86-64.so.2 --library-path /opt/compiler/gcc-10/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.2/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib"
pyt="/ssd2/liuyixin04/miniconda3/envs/py37_torch/bin/python"
export CUDA_VISIBLE_DEVICES=3

$lib $pyt generate_rem.py \
    --arch resnet18 \
    --dataset mnist-mini \
    --train-steps 703 \
    --batch-size 128 \
    --optim sgd \
    --lr 0.1 \
    --lr-decay-rate 0.1 \
    --lr-decay-freq 2000 \
    --weight-decay 5e-4 \
    --momentum 0.9 \
    --pgd-radius 8 \
    --pgd-steps 10 \
    --pgd-step-size 1.6 \
    --pgd-random-start \
    --atk-pgd-radius 4 \
    --atk-pgd-steps 10 \
    --atk-pgd-step-size 0.8 \
    --atk-pgd-random-start \
    --samp-num 5 \
    --report-freq 1000 \
    --save-freq 1000 \
    --data-dir ./data \
    --save-dir ./exp_data/mnist/noise-test/rem8-4 \
    --save-name rem \
    --parallel