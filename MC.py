#!/usr/bin/env python

import sys
import math
import numpy
import random
import xml.etree.ElementTree as ET

# HBV
# file_experiment = ["hbv5.4um.csv", "hbv8.2um.csv", "hbv10.8um.csv"]
# k = 1
# concentration = [5.4, 8.2, 10.8]
# xml_filename = ["hbv600_5.4um.xml", "hbv600_8.2um.xml", "hbv600_10.8um.xml"]

# HPV
file_experiment = ["hpv0.53um.csv", "hpv0.72um.csv", "hpv0.80um.csv"]
k = 7.04e-08
concentration = [0.53, 0.72, 0.80]
xml_filename = ["hpv360_0.53um.xml", "hpv360_0.72um.xml", "hpv360_0.80um.xml"]

# CCMV
# file_experiment = ["ccmv14.1um.csv", "ccmv15.6um.csv", "ccmv18.75um.csv"]
# k = 1 one k per concentration
# concentration = [14.1, 15.6, 18.75]
# xml_filename = ["ccmv450_14.1um.xml", "ccmv450_15.6um.xml", "ccmv450_18.75um.xml"]

def read_from_file(filename):
	data_file = filename
	datafile = open(data_file, "r")
	data_raw = datafile.readlines()
	datafile.close()
	return data_raw

def java_to_list(data_raw):
	data = [map(eval, x.strip().split()) for i, x in enumerate(data_raw) if i not in [0, 1]]
	return data

def parse_csv(filename):
	data_raw = read_from_file(filename)
	data_experiment = [map(eval, x.strip().split()) for x in data_raw]
	return data_experiment

def light_scattering(data_time_t, c):
	st = float(sum([y*i*i for i, y in enumerate(data_time_t)])) / float(sum([y*i for i, y in enumerate(data_time_t)]))
	return k * concentration[c] * st

def parse_java_50(time, c):
	sls_all_50 = [[] for i in range(len(time))]
	for i in range(1, 51): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		print i, c
		filename = "java_" + str(concentration[c]) + "_" + str(i) + ".txt"
		data_raw = read_from_file(filename)
		data_simulate = java_to_list(data_raw)
		j = 0
		for k, x in enumerate(time):
			while data_simulate[j][0] < x:
				j += 1
			sls_all_50[k].append(light_scattering(data_simulate[j], c))
	sls_avg = [numpy.mean(x) for x in sls_all_50]
	return sls_avg

def energy_temp(sls_avg, data_experiment):
	return sum([(x - y[0][1])**2 for x, y in zip(sls_avg, data_experiment)]) / len(data_experiment)

def energy(energy_temp_all):
	energy_candidate = math.sqrt(sum(energy_temp_all) / len(energy_temp_all))
	return energy_candidate

def current():
	data_raw = read_from_file("current.txt")
	return map(eval, data_raw[0].strip().split())

def candidate():
	data_raw = read_from_file("candidate.txt")
	return map(eval, data_raw[0].strip().split())

# True: move; False: stay
def move(energy_candidate, energy_current):
	if energy_candidate <= energy_current:
		return True
	else:
		kk = 1
		T = 1
		prob = math.exp((energy_current - energy_candidate) / (kk * T))
		if random.uniform(0, 1) < prob:			
			return True
		else:
			return False

def write_current_file(now):
	current_file = open("current.txt", "w")
	current_file.write("\t".join([str(x) for x in now]))

def write_series_file(now):
	series_file = open("series.txt", "a")
	series_file.write("\n" + "\t".join([str(x) for x in now[:-1]]))

def disturbe(parameter_set):
	parameter_number = len(parameter_set)
	disturbe_index = int(random.uniform(0, parameter_number))
	disturbe_scale = random.uniform(0.5, 1.5)
	parameter_set[disturbe_index] *= disturbe_scale
	return parameter_set

def write_candidate_file(new_candidate):
	current_file = open("candidate.txt", "w")
	current_file.write("\t".join([str(x) for x in new_candidate]))

# HBV modify
# def modify_xml(new_candidate, c):
# 	tree = ET.parse(xml_filename[c])
# 	root = tree.getroot()
# 	for i in range(len(new_candidate)):
# 		part = root[2][i][1]
# 		part.set('bindTime', str(new_candidate[(i % 4) * 2]))
# 		part.set('breakTime', str(new_candidate[(i % 4) * 2 + 1]))
# 	tree.write(xml_filename[c])

# HPV modify
def modify_xml(new_candidate, c):
	tree = ET.parse(xml_filename[c])
	root = tree.getroot()
	for i in range(len(new_candidate) / 2):
		if i == 0:
			for j in range(1, 6):
				part = root[2][5][j]
				part.set('bindTime', str(new_candidate[0]))
				part.set('breakTime', str(new_candidate[1]))
			for j in range(6, 11):
				part = root[2][j][1]
				part.set('bindTime', str(new_candidate[0]))
				part.set('breakTime', str(new_candidate[1]))
		elif i == 1:
			for j in range(2):
				part = root[2][j][1]
				part.set('bindTime', str(new_candidate[2]))
				part.set('breakTime', str(new_candidate[3]))
		elif i == 2:
			for j in range(2, 4):
				part = root[2][j][1]
				part.set('bindTime', str(new_candidate[4]))
				part.set('breakTime', str(new_candidate[5]))
		elif i == 3:
			part = root[2][4][1]
			part.set('bindTime', str(new_candidate[6]))
			part.set('breakTime', str(new_candidate[7]))
	tree.write(xml_filename[c])

# CCMV modify
def modify_xml(new_candidate, c):
	tree = ET.parse(xml_filename[c])
	root = tree.getroot()
	for i in range(len(new_candidate) / 2):
		if i == 0:
			for j in [1, 2]:
				part1 = root[2][0][j]
				part1.set('bindTime', str(new_candidate[0]))
				part1.set('breakTime', str(new_candidate[1]))
				part2 = root[2][3 + j * 2][1]
				part2.set('bindTime', str(new_candidate[0]))
				part2.set('breakTime', str(new_candidate[1]))
		if i == 1:
			for j in [1, 2]:
				part1 = root[2][1][j]
				part1.set('bindTime', str(new_candidate[2]))
				part1.set('breakTime', str(new_candidate[3]))
				part2 = root[2][3 + j * 2 - 1][1]
				part2.set('bindTime', str(new_candidate[2]))
				part2.set('breakTime', str(new_candidate[3]))
		if i == 2:
			for j in [2, 3]:
				part = root[2][j][1]
				part.set('bindTime', str(new_candidate[4]))
				part.set('breakTime', str(new_candidate[5]))
	tree.write(xml_filename[c])

if __name__ == "__main__":
	energy_temp_all = []
	for i, temp in enumerate(file_experiment):
		data_experiment = parse_csv(temp)
		time = [x[0][0] for x in data_experiment]
		# Read 50 .txt files from java out put. java_concentration_index.txt, index in [1,50]. (result from simulate candidate)
		# Each turn into light scattering. Calculate average. 
		sls_avg = parse_java_50(time, i)
		e = energy_temp(sls_avg, data_experiment)
		energy_temp_all.append(e)
	energy_candidate = energy(energy_temp_all)		
	# Get current parameter info.
	energy_current = current()[-1]
	# Decide move or not, if move, change current
	if move(energy_candidate, energy_current):
		now = candidate()
		now.append(energy_candidate)
		write_current_file(now)
	else:
		now = current()
	# Write now into series
	write_series_file(now)
	# disturbe now, get new parameter set
	new_candidate = disturbe(now[:-1])
	# Write into candidate.txt and modify .xml
	write_candidate_file(new_candidate)
	factor = [concentration[0] / x for x in concentration]
	for i, temp in enumerate(factor):
		new_candidate_scale = []
		for j, x in enumerate(new_candidate):
			if j % 2 ==0:
				new_candidate_scale.append(x * factor[i])
			else:
				new_candidate_scale.append(x)
		modify_xml(new_candidate_scale, i)