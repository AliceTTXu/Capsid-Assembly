#!/bin/bash


header="#!/bin/bash"
msg='queueing'
dir="/home/tingtinx/HPV"

For i in `seq 10000`
do
	For j in `seq 50`
	do 
		echo $msg 'chr '
		header1="#PBS -e $dir/err/test.err\n"
		header2="#PBS -o $dir/out/test.out\n"
		header3="#PBS -l nodes=1:ppn=1\n"
		header4="#PBS -l walltime=24:00:00"
		commandstr="cd $dir\n java -cp .:vecmath-1.5.2.jar Test hpv360.xml 1 23000 $RANDOM 120 > java_${j}"
		echo -e $header"\n\n"$header1$header2$header3header4"\n"$commandstr > test_0.53${j}.job
		qsub -q rs1 test_0.53${j}.job
		rm test_0.53${j}.job
	done
	
	while [[ 1 ]]; do
		sleep 1
		qstat -u tingtinx > njob.txt
		temp = wc -l njob.txt | awk '{print $l}'
		if [[ $temp == 6 ]]; then
			break
		fi
	done
	python hpv.py
done