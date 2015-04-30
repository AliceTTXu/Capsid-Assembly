#!/bin/bash

header="#!/bin/bash"
msg='queueing'
dir="~/HBV"

echo -e '#PBS -e main.err' > main.job
echo -e '#PBS -o main.out' >> main.job
echo -e '
#PBS -l nodes=1:ppn=4
#PBS -l walltime=192:00:00
#PBS -q rs1
cd $PBS_O_WORKDIR' >> main.job

commandstr='bash ./hbv_simulate.sh'
echo -e $commandstr >> main.job
qsub -q rs1 main.job
rm main.job
