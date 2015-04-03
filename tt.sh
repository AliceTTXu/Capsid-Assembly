#!/bin/bash

header="#!/bin/bash"
msg='queueing'
dir="/home/tingtinx/HPV"

#while read -u3 filename
for i in {1..50}
do
  header1="#PBS -e $dir/err/filter_${i}.err\n"
  header2="#PBS -o $dir/out/filter_${i}.out\n"
  header3="#PBS -l nodes=1:ppn=1\n"
 # header4="#PBS -l walltime=23:00"
  echo Processing $i
  commandstr="cd $dir/code\n java -cp .:vecmath-1.5.2.jar Test hpv360.xml 1 23000 $RANDOM 72 > java_"${j}".txt;exit"
  echo -e $header"\n\n"$header1$header2$header3"\n"$commandstr > run_${i}.job
  qsub -q pool1 run_${i}.job
  rm run_${i}.job
done