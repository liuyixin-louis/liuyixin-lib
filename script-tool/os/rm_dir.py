import os
import shutil
path="/ssd2/liuyixin04/workspace/logs/benchmark-torch/train_log/"
filestr="True"
# find $path -name "$*filestr"|xargs rm -rfv
for p,d,f in os.walk(path):
    if 'True' in p:
        # print(p)
        shutil.rmtree(path=p)