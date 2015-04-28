header="#!/bin/bash"
msg='queueing'

for i in `seq 1000`
	do
	for j in `seq 50`
		do 
		echo -e '#PBS -e err_0.53_'${j}'.error' > simulate_0.53_${j}.job
		echo -e '#PBS -o out_0.53_'${j}'.txt' >> simulate_0.53_${j}.job
		echo -e '
		#PBS -l nodes=1:ppn=4
		#PBS -l walltime=24:00:00
		#PBS -q rs1
		cd $PBS_O_WORKDIR' >> simulate_0.53_${j}.job

		commandstr='java -cp .:vecmath-1.5.2.jar Test hpv360_0.53um.xml 1 12000 $RANDOM 72 > java_0.53_'${j}'.txt\npython pre.py java_0.53_'${j}'.txt'
		echo -e $commandstr >> simulate_0.53_${j}.job
		qsub -q rs1 simulate_0.53_${j}.job
		rm simulate_0.53_${j}.job
		done
	for j in `seq 50`
                do
                echo -e '#PBS -e err_0.72_'${j}'.error' > simulate_0.72_${j}.job
                echo -e '#PBS -o out_0.72_'${j}'.txt' >> simulate_0.72_${j}.job
                echo -e '
                #PBS -l nodes=1:ppn=4
                #PBS -l walltime=24:00:00
                #PBS -q rs1
                cd $PBS_O_WORKDIR' >> simulate_0.72_${j}.job

                commandstr='java -cp .:vecmath-1.5.2.jar Test hpv360_0.72um.xml 1 15000 $RANDOM 72 > java_0.72_'${j}'.txt\npython pre.py java_0.72_'${j}'.txt'
                echo -e $commandstr >> simulate_0.72_${j}.job
                qsub -q rs1 simulate_0.72_${j}.job
                rm simulate_0.72_${j}.job
                done
	for j in `seq 50`
                do
                echo -e '#PBS -e java_0.8_'${j}'.error' > simulate_0.8_${j}.job
                echo -e '#PBS -o java_0.8_'${j}'.txt' >> simulate_0.8_${j}.job
                echo -e '
                #PBS -l nodes=1:ppn=4
                #PBS -l walltime=24:00:00
                #PBS -q rs1
                cd $PBS_O_WORKDIR' >> simulate_0.8_${j}.job

                commandstr='java -cp .:vecmath-1.5.2.jar Test hpv360_0.80um.xml 1 15000 $RANDOM 72 > java_0.8_'${j}'.txt\npython pre.py java_0.8_'${j}'.txt'
                echo -e $commandstr >> simulate_0.8_${j}.job
                qsub -q rs1 simulate_0.8_${j}.job
                rm simulate_0.8_${j}.job
                done
	
	while [[ 1 ]]; do
		sleep 1
		qstat -u tingtinx > njob.txt
		temp=$(wc -l njob.txt | awk '{print $1}')
		if [[ $temp == 6 ]]; then
			break
		fi
	done
	
	qsub -q rs1 move.job
	
	while [[ 1 ]]; do
                sleep 1
                qstat -u tingtinx > njob.txt
                temp=$(wc -l njob.txt | awk '{print $1}')
		if [[ $temp == 6 ]]; then
                        break
                fi
        done

done
