import xml.etree.ElementTree as ET

new_candidate = [1.2, 1.4, 2.4, 2.3, 3.4, 3.7, 4.7, 4.5]

tree = ET.parse("hpv360_0.53um.xml")
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
	tree.write("hpv360_0.53um.xml")