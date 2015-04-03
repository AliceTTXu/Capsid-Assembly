header="#!/bin/bash"
msg='queueing'
dir="/home/tingtinx/HPV"

for j in `seq 50`
do 
	echo $msg 'chr '
	header1="#PBS -e $dir/err/test.err\n"
	header2="#PBS -o $dir/out/test.out\n"
	header3="#PBS -l nodes=1:ppn=1\n"
	header4="#PBS -l walltime=24:00:00"
	commandstr="cd $dir\n java -cp .:vecmath-1.5.2.jar Test hpv360.xml 1 23000 $RANDOM 72 > java_"${j}".txt"
	echo -e $header"\n\n"$header1$header2$header3$header4"\n"$commandstr > test_${j}.job
	qsub -q rs1 test_${j}.job
	rm test_${j}.job
done