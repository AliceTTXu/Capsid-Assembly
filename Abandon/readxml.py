#!/usr/bin/env python

import sys
import math
import xml.etree.ElementTree as ET

if __name__ == "__main__":
	new_candidate = [111, 222, 333, 444, 555, 666, 777, 888]
	tree = ET.parse('hbv600.xml')
	root = tree.getroot()
	for i in range(len(new_candidate)):
		part = root[2][i][1]
		part.set('bindTime', str(new_candidate[(i % 4) * 2]))
		part.set('breakTime', str(new_candidate[(i % 4) * 2 + 1]))
	tree.write('output.xml')