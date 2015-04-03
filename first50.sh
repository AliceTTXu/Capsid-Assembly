header="#!/bin/bash"
msg='queueing'
dir="/home/tingtinx/HPV"

for j in `seq 50`
do 
echo -e '#PBS -e java_'${j}'.error' > test_${j}.job
echo -e '#PBS -o java_'${j}'.txt' >> test_${j}.job
echo -e '
#PBS -l nodes=1:ppn=1
#PBS -l walltime=24:00:00
#PBS -q rs1
cd $PBS_O_WORKDIR' >> test_${j}.job

commandstr='java -cp .:vecmath-1.5.2.jar Test hpv360.xml 1 23000 $RANDOM 72'
echo -e $commandstr >> test_${j}.job
qsub -q rs1 test_${j}.job
rm test_${j}.job
done
