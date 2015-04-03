#!/usr/bin/env python

import sys
import math
import numpy
import random
import xml.etree.ElementTree as ET

# HPV
file_experiment = ["hpv0.53um.csv", "hpv0.72um.csv", "hpv0.80um.csv"]
k = 7.04e-08
concentration = [0.53, 0.72, 0.80]
xml_filename = "hpv360.xml"

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
	one_experiment = [[], []]
	one_experiment[0] = [x[0][0] for x in data_experiment]
	one_experiment[1] = [x[0][1] for x in data_experiment]
	return one_experiment

def light_scattering(data_time_t, c):
	st = float(sum([y*i*i for i, y in enumerate(data_time_t)])) / float(sum([y*i for i, y in enumerate(data_time_t)]))
	return k * concentration[c] * st

def parse_java_50(time, c, fac):
	sls_all_50 = [[] for i in range(len(time))]
	for i in range(1, 2): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		filename = "java_" + str(i) + ".txt"
		data_raw = read_from_file(filename)
		data_simulate = java_to_list(data_raw)
		j = 0
		for i, x in enumerate(time):
			while data_simulate[j][0] * fac < x:
				j += 1
			sls_all_50[i].append(light_scattering(data_simulate[j], c))
	sls_avg = [numpy.mean(x) for x in sls_all_50]
	return sls_avg

def energy(experiment, sls):
	avg_sum = []
	for i in range(len(experiment)):
		temp = sum([(x - y)**2 for x, y in zip(experiment[i][1], sls[i])]) / experiment[i][0][-1]
		avg_sum.append(temp)
	return math.sqrt(sum(avg_sum) / len(experiment))

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
	series_file.write("\n" + "\t".join([str(x) for x in now]))

def disturbe(parameter_set):
	parameter_number = len(parameter_set)
	disturbe_index = int(random.uniform(0, parameter_number))
	disturbe_scale = random.uniform(0.5, 1.5)
	parameter_set[disturbe_index] *= disturbe_scale
	return parameter_set

def write_candidate_file(new_candidate):
	current_file = open("candidate.txt", "w")
	current_file.write("\t".join([str(x) for x in new_candidate]))

# HPV modify
def modify_xml(new_candidate):
	tree = ET.parse(xml_filename)
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
		tree.write(xml_filename)

if __name__ == "__main__":
	# Hold experiment data
	experiment = []
	# Hold simulation data
	sls = []
	factor = [concentration[0] / x for x in concentration]
	for i, temp in enumerate(file_experiment):
		experiment.append(parse_csv(temp))
		# Read 50 .txt files from java out put. java_index.txt, index in [1,50]. (result from simulate candidate)
		# Each turn into light scattering. Calculate average.
		# Parse for different concentration accordingly, concentration specified by factor vector
		sls.append(parse_java_50(experiment[i][0], i, factor[i]))
	energy_candidate = energy(experiment, sls)
	# Get current parameter info.
	energy_current = current()[-1]
	# Decide move or not, if move, change current
	if move(energy_candidate, energy_current):
		now = candidate()
		now.append(energy_candidate)
		write_current_file(now)
	else:
		now = current()
	# Write current into series
	write_series_file(now)
	# disturbe current, get new parameter set
	new_candidate = disturbe(now[:-1])
	# Write into candidate.txt and modify .xml
	write_candidate_file(new_candidate)
	modify_xml(new_candidate)