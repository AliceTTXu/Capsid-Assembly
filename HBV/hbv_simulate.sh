header="#!/bin/bash"
msg='queueing'

for i in `seq 1000`
	do
	for j in `seq 50`
		do 
		echo -e '#PBS -e err_5.4_'${j}'.error' > simulate_5.4_${j}.job
		echo -e '#PBS -o out_5.4_'${j}'.txt' >> simulate_5.4_${j}.job
		echo -e '
		#PBS -l nodes=1:ppn=4
		#PBS -l walltime=24:00:00
		#PBS -q rs1
		cd $PBS_O_WORKDIR' >> simulate_5.4_${j}.job

		commandstr='java -cp .:vecmath-1.5.2.jar Test hbv600_5.4um.xml 4000 550 $RANDOM 120 > java_5.4_'${j}'.txt\npython pre.py java_5.4_'${j}'.txt'
		echo -e $commandstr >> simulate_5.4_${j}.job
		qsub -q rs1 simulate_5.4_${j}.job
		rm simulate_5.4_${j}.job
		done
	for j in `seq 50`
                do
                echo -e '#PBS -e err_8.2_'${j}'.error' > simulate_8.2_${j}.job
                echo -e '#PBS -o out_8.2_'${j}'.txt' >> simulate_8.2_${j}.job
                echo -e '
                #PBS -l nodes=1:ppn=4
                #PBS -l walltime=24:00:00
                #PBS -q rs1
                cd $PBS_O_WORKDIR' >> simulate_8.2_${j}.job

                commandstr='java -cp .:vecmath-1.5.2.jar Test hpv600_8.2um.xml 4000 550 $RANDOM 120 > java_8.2_'${j}'.txt\npython pre.py java_8.2_'${j}'.txt'
                echo -e $commandstr >> simulate_8.2_${j}.job
                qsub -q rs1 simulate_8.2_${j}.job
                rm simulate_8.2_${j}.job
                done
	for j in `seq 50`
                do
                echo -e '#PBS -e java_10.8_'${j}'.error' > simulate_10.8_${j}.job
                echo -e '#PBS -o java_10.8_'${j}'.txt' >> simulate_10.8_${j}.job
                echo -e '
                #PBS -l nodes=1:ppn=4
                #PBS -l walltime=24:00:00
                #PBS -q rs1
                cd $PBS_O_WORKDIR' >> simulate_10.8_${j}.job

                commandstr='java -cp .:vecmath-1.5.2.jar Test hbv600_10.8um.xml 4000 550 $RANDOM 120 > java_10.8_'${j}'.txt\npython pre.py java_10.8_'${j}'.txt'
                echo -e $commandstr >> simulate_10.8_${j}.job
                qsub -q rs1 simulate_10.8_${j}.job
                rm simulate_10.8_${j}.job
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
