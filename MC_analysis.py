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

def stat(data):
	total = len(data)
	center = data[1]
	print center
	interval_count = []
	for i in range(1, 10):
		interval_size = float(i) / 10
		up = [x * (1.0 + interval_size) for x in center]
		low = [x * (1.0 - interval_size) for x in center]
		print up, low
		cat = []
		for j, x in enumerate(data):
			if len(x) == sum(y[0] <= y[1] and y[1] <= y[2] for y in zip(low, x, up)):
				cat.append(j)
		interval_count.append(len(cat) / total)
		data = [x[1] for x in enumerate(data) if x[0] not in cat]
	interval_count.append(1 - sum(interval_count))
	return interval_count

if __name__ == "__main__":
	filename = "series.txt"
	datafile = open(filename, "r")
	data_raw = datafile.readlines()
	datafile.close()
	data = parse(data_raw)	
	print(stat(data))