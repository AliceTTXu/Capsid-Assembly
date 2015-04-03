header="#!/bin/bash"
msg='queueing'
dir="/home/tingtinx/HPV"

RANDOM=40

for j in `seq 50`
do 
	echo $msg 'chr '
	echo "#PBS -e $dir/err/test.err
	#PBS -o $dir/out/test.out
	#PBS -l nodes=1:ppn=1
	#PBS -l walltime=24:00:00
	cd $dir
	java -cp .:vecmath-1.5.2.jar Test hpv360.xml 1 23000 $RANDOM 72 > java_"${j}".txt
	" > test_${j}.job
	#qsub -q rs1 test_${j}.job
	#rm test_${j}.job
done
