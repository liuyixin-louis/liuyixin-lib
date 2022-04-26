cd /ssd2/liuyixin04/workspace/yixin-library/project/robust_noise/
so="/opt/compiler/gcc-8.2/lib/ld-linux-x86-64.so.2"
lib="/opt/compiler/gcc-8.2/lib:/usr/lib64:/ssd2/liuyixin04/miniconda3/envs/py37_paddle/lib:/home/work/cuda-10.0/lib64/:/home/work/cudnn_v7.4/cuda/lib64/:/ssd2/liuyixin04/.jumbo/lib"
py="/ssd2/liuyixin04/miniconda3/envs/py37_torch/bin/python"
# cmd="torch.distributed.run --nnodes=1 --nproc_per_node=2 --node_rank=0  --master_port=6005"
# patchelf --set-interpreter $so --set-rpath $lib $py
$so --library-path $lib $py generate.py \
    --arch resnet18 \
    --dataset cifar10 \
    --train-steps 5000 \
    --batch-size 8 \
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
    --save-dir ./exp_data/cifar10/noise/rem8-4 \
    --save-name rem \
    --attacker pgd \
    --parallel
    # --cpu
# $so --library-path  $lib $py train.py \
#     --arch resnet18 \
#     --dataset cifar10 \
#     --train-steps 40000 \
#     --batch-size 128 \
#     --optim sgd \
#     --lr 0.1 \
#     --lr-decay-rate 0.1 \
#     --lr-decay-freq 16000 \
#     --weight-decay 5e-4 \
#     --momentum 0.9 \
#     --pgd-radius 4 \
#     --pgd-steps 10 \
#     --pgd-step-size 0.8 \
#     --pgd-random-start \
#     --report-freq 1000 \
#     --save-freq 100000 \
#     --noise-path ./exp_data/cifar10/noise/rem8-4/rem-fin-def-noise.pkl \
#     --data-dir ./data \
#     --save-dir ./exp_data/cifar10/train/rem8-4/r4 \
#     --save-name train \
#     --parallel