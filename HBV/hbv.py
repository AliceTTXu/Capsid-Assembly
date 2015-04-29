#!/usr/bin/env python

import sys
import math
import numpy
import random
import xml.etree.ElementTree as ET

# HBV
file_experiment = ["hbv5.4um_s.csv", "hbv8.2um_s.csv", "hbv10.8um_s.csv"]
concentration = [5.4, 8.2, 10.8]
xml_filename = ["hbv600_5.4um.xml", "hbv600_8.2um.xml", "hbv600_10.8um.xml"]

def read_from_file(filename):
	data_file = filename
	datafile = open(data_file, "r")
	data_raw = datafile.readlines()
	datafile.close()
	return data_raw

def pre_to_list(data_raw):
	data = [map(eval, x.strip().split()) for x in data_raw]
	return data

def parse_csv(filename):
	data_raw = read_from_file(filename)
	data_experiment = [map(eval, x.strip().split()) for x in data_raw]
	return data_experiment

def parse_java_50(time, c):
	sls_all_50 = [[] for i in range(len(time))]
	for i in range(1, 2): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		filename = "sls_" + str(concentration[c]) + "_" + str(i) + ".txt"
		data_raw = read_from_file(filename)
		data_simulate = pre_to_list(data_raw)
		for j, x in enumerate(data_simulate):
			sls_all_50[j].append(x)
	sls_avg = [numpy.mean(x) for x in sls_all_50]
	return sls_avg

def kcal_pre(data_experiment, sls_avg, c):
	temp_up = [x[0][1] * (y - 1) for x, y in zip(data_experiment, sls_avg)]
	temp_down = [(y - 1)**2 for x, y in zip(data_experiment, sls_avg)]
	up = concentration[c] * sum(temp_up) / len(temp_up)
	down = (concentration[c]**2) * sum(temp_down) / len(temp_down)
	return (up, down)

def kcal(pre_k_all):
	k = sum([x[0] for x in pre_k_all]) / sum([x[1] for x in pre_k_all])
	return k

def energy_temp(data_experiment, sls_avg, k, c):
	return sum([(x[0][1] + k * concentration[c] - k * concentration[c] * y)**2 for x, y in zip(data_experiment, sls_avg)]) / len(data_experiment)

def energy(energy_temp_all):
	energy_candidate = sum([math.sqrt(x) for x in energy_temp_all]) / len(energy_temp_all)
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
	parameter_number = len(parameter_set) / 2 + 1
	disturbe_index = int(random.uniform(0, parameter_number))
	disturbe_scale = random.uniform(0.95, 1.05)
	if disturbe_index == 0:
		for i in range(len(parameter_set)):
			if i % 2 == 0:
				parameter_set[i] *= disturbe_scale
	else:
		parameter_set[2 * disturbe_index - 1] *= disturbe_scale
	return parameter_set

def write_candidate_file(new_candidate):
	current_file = open("candidate.txt", "w")
	current_file.write("\t".join([str(x) for x in new_candidate]))
	current_file.close()

# HBV modify
def modify_xml(new_candidate, c):
	tree = ET.parse(xml_filename[c])
	root = tree.getroot()
	for i in range(len(new_candidate)):
		part = root[2][i][1]
		part.set('bindTime', str(new_candidate[(i % 4) * 2]))
		part.set('breakTime', str(new_candidate[(i % 4) * 2 + 1]))
	tree.write(xml_filename[c])

if __name__ == "__main__":
	data_all = []
	pre_k_all = []
	for i, temp in enumerate(file_experiment):
		data_experiment = parse_csv(temp)
		time = [x[0][0] for x in data_experiment]
		# Read 50 .txt files from java out put. java_concentration_index.txt, index in [1,50]. (result from simulate candidate)
		# Each turn into light scattering. Calculate average. 
		sls_avg = parse_java_50(time, i)
		data_all.append((data_experiment, sls_avg))
		# pre calculate the single k to share among all concentration
		pre_k = kcal_pre(data_experiment, sls_avg, i)
		pre_k_all.append(pre_k)
	# calculate k
	k = kcal(pre_k_all)
	energy_temp_all = []
	for i, x in enumerate(data_all):
		e = energy_temp(x[0], x[1], k, i)
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