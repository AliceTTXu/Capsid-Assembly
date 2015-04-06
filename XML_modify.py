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

if __name__ == "__main__":
	new_candidate = [1e6, 10, 1e6, 10, 1e6, 10, 1e6, 10]
	factor = [concentration[0] / x for x in concentration]
	print factor
	for i, temp in enumerate(factor):
		new_candidate_scale = []
		for j, x in enumerate(new_candidate):
			if j % 2 ==0:
				new_candidate_scale.append(x * factor[i])
			else:
				new_candidate_scale.append(x)
		print new_candidate_scale
		modify_xml(new_candidate_scale, i)