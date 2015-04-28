#!/usr/bin/env python

import sys

# HBV
file_experiment = ["hbv5.4um.csv", "hbv8.2um.csv", "hbv10.8um.csv"]
file_experiment_shift = ["hbv5.4um_s.csv", "hbv8.2um_s.csv", "hbv10.8um_s.csv"]

def read_from_file(filename):
	data_file = filename
	datafile = open(data_file, "r")
	data_raw = datafile.readlines()
	datafile.close()
	return data_raw

def parse_csv(filename):
	data_raw = read_from_file(filename)
	data_experiment = [map(eval, x.strip().split()) for x in data_raw]
	return data_experiment

def write_file(data, filename):
	current_file = open(filename, "w")
	current_file.write("\n".join([str(x) for x in data]))
	current_file.close()

if __name__ == "__main__":
	for i, x in enumerate(file_experiment):
		data_experiment = parse_csv(x)
		shift = data_experiment[0][0][1]
		data_experiment_shift = [",".join([str(y[0][0]), str(y[0][1] - shift)]) for y in data_experiment]
		write_file(data_experiment_shift, file_experiment_shift[i])