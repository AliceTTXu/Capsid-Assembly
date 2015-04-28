#!/usr/bin/env python

import sys
import math

file_experiment = ["hbv5.4um.csv", "hbv8.2um.csv", "hbv10.8um.csv"]
concentration = [5.4, 8.2, 10.8]

def read_from_file(filename):
	data_file = filename
	datafile = open(data_file, "r")
	data_raw = datafile.readlines()
	datafile.close()
	return data_raw

def java_to_list(data_raw):
	data = [map(eval, x.strip().split()) for i, x in enumerate(data_raw) if i not in [0, 1]]
	return data

def light_scattering(data_time_t, c):
	st = float(sum([y*i*i for i, y in enumerate(data_time_t)])) / float(sum([y*i for i, y in enumerate(data_time_t)]))
	return concentration[c] * st

def parse_csv(filename):
	data_raw = read_from_file(filename)
	data_experiment = [map(eval, x.strip().split()) for x in data_raw]
	return data_experiment

def java_to_sls(data_simulate, time, c):
	sls = []
	j = 0
	for i, x in enumerate(time):
		while data_simulate[j][0] < x:
			j += 1
		sls.append(light_scattering(data_simulate[j], c))
	return sls

def decide(filename):
	temp = list(filename)
	try:
		cat = float("".join(temp[5:9]))
	except ValueError:
		cat = float("".join(temp[5:8]))
	for i, x in enumerate(concentration):
		if cat == x:
			return i

def write_sls(sls, filename):
	temp = list(filename)
	filename = "sls" + filename[4:]
	filename = "".join(filename)
	sls_file = open(filename, "w")
	sls_file.write("\n".join([str(x) for x in sls]))
	sls_file.close()

if __name__ == "__main__":
	filename = sys.argv[1]
	category = decide(filename)
	data_raw = read_from_file(filename)
	data_simulate = java_to_list(data_raw)
	data_experiment = parse_csv(file_experiment[category])
	time = [x[0][0] for x in data_experiment]
	sls = java_to_sls(data_simulate, time, category)
	write_sls(sls, filename)
