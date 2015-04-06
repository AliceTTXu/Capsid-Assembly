#!/usr/bin/env python

import sys
import math
import random

# random.seed(1)

def parse_in(data_raw):
	return map(float, data_raw.strip().split()[:-1])

def findNeighbour(parameter_set):
	parameter_number = len(parameter_set)
	disturbe_index = int(random.uniform(0, parameter_number))
	disturbe_scale = random.uniform(0.5, 1.5)
	parameter_set[disturbe_index] *= disturbe_scale
	return parameter_set

def parse_out(parameter_new):
	parameter_new = [str(x) for x in parameter_new]
	return "\t".join(parameter_new)

if __name__ == "__main__":
	para_file = "parameter_two.txt"
	para_old = open(para_file, "r")
	para_old_raw = para_old.read()
	para_old.close()
	parameter_old = parse_in(para_old_raw)
	parameter_new = findNeighbour(parameter_old)
	parameter_string = parse_out(parameter_new)
	para_new = open(para_file, "a")
	para_new.write("\n" + parameter_string)
	para_new.close()