header="#!/bin/bash"
msg='queueing'
dir="/home/tingtinx/HPV"
echo $msg 'chr'
header1="#PBS -e $dir/err/test.err\n"
header2="#PBS -o $dir/out/test.out\n"
header3="#PBS -l nodes=1:ppn=1\n"
header4="#PBS -l walltime=24:00:00"
commandstr="cd $dir\n javac -cp vecmath-1.5.2.jar *.java;exit"
echo -e $header"\n\n"$header1$header2$header3$header4"\n"$commandstr > test.job
qsub -q rs1 test.job
rm test.job