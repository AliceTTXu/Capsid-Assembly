#!/usr/bin/env python

import sys
import math
import random

def parse(data_raw):
	data = []
	for i, x in enumerate(data_raw):
		x = map(float, x.strip().split())
		data.append(x)
	return data

def move(data):
	energy0 = data[0][-1]
	energy1 = data[1][-1]
	if energy0 >= energy1:
		data = data[1]
	else:
		k = 1
		T = 1
		prob = math.exp((energy0 - energy1) / (k * T))
		if random.uniform(0, 1) < prob:
			data = data[1]
		else:
			data = data[0]
	data = [str(x) for x in data]
	return data

if __name__ == "__main__":
	filename = "parameter_two.txt"
	datafile = open(filename, "r")
	data_raw = datafile.readlines()
	datafile.close()
	data = parse(data_raw)
	para_current = move(data)
	para_two = open(filename, "w")
	para_two.write("\t".join(para_current))
	para_two.close
	para_series = open("parameter_series.txt", "a")
	para_series.write("\n" + "\t".join(para_current[:-1]))
