
ps -ef|grep "/ssd2/liuyixin04/miniconda3/envs/py37_paddle/bin/python"|grep -v grep|awk '{print "kill -9 "$2}'
rm -r /ssd2/liuyixin04/workspace/logs/benchmark-paddle

ps -ef|grep "/ssd2/liuyixin04/miniconda3/envs/py37_torch/bin/python"|grep -v grep|awk '{print "kill -9 "$2}'
rm -r /ssd2/liuyixin04/workspace/logs/benchmark-torch