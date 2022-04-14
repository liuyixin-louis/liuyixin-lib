i=0
gpu=(1 2 3 4 5 6 7)
while [ 1 ]
do
i=`expr $i % 7`
echo ${gpu[$i]}
i=`expr $i + 1`
done