#!/usr/bin/env python

import sys
import math

def read_in_data(filename):
	data_file = filename
	datafile = open(data_file, "r")
	data_raw = datafile.readlines()
	datafile.close()
	return data_raw

def parse(data_raw):
	data = []
	for i, x in enumerate(data_raw):
		if i not in [0, 1]:
			x = map(eval, x.strip().split())
			data.append(x)
	return data

def light_scattering(data):
	# (P24 4.1)
	k = 1
	c = 5.4
	sls = []
	for x in data:
		st = float(sum([y*i*i for i, y in enumerate(x)])) / float(sum([y*i for i, y in enumerate(x)]))
		sls.append([x[0], k*c*st])
	return sls

def ref_lab():
	lab_raw = read_in_data("hbv5.4um.csv")
	lab = []
	for x in lab_raw:
		lab.append(map(eval, x.strip().split()))
	return lab

def energy(sls):
	# preprocess sls
	# sls_select = []
	lab = ref_lab()
	j = 0
	pairs = []
	for x in lab:
		while sls[j][0] < x[0][0]:
			j += 1
		pairs.append([x[0][1], sls[j][1]])
	# sum_time = sum([(x[1] - y[1])**2 for x, y in zip(sls, lab)])
	# if more than one concentration
	# avg_concentration = sum(sum_time / sls[-1][0]) / len(sum_time)
	# e = math.sqrt(sum_time)
	return pairs

if __name__ == "__main__":	
	sls_data_raw = read_in_data("java_2.txt")
	sls_data = parse(sls_data_raw)
	sls = light_scattering(sls_data)
	# print(sls)
	# print(energy(sls))
	# print(ref_lab()[100][0][0])
	# lab_raw = read_in_data("test_lab.txt")
	# lab = parse(lab_raw)
	# print(sls)
	# print(lab)
	# e = energy(sls, lab)
	# para_file = "parameter_two.txt"
	# para_new = open(para_file, "a")
	# para_new.write("\t" + str(e))
	# para_new.close()