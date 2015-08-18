import csv
from lxml import etree
import os
from os.path import join
import re

path = 'demo_eads_normalized'

undated = re.compile(r'^[Uu]ndated$')

for filename in os.listdir(path):	
	tree = etree.parse(join(path,filename))
	unitdates = tree.xpath('//unitdate')
	for unitdate in unitdates:
		if unitdate.text is not None:
			if not 'normal' in unitdate.attrib and not undated.match(unitdate.text):
				date = unitdate.text
				date_path = tree.getpath(unitdate)
				with open('non-normalized_unitdates.csv','ab') as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow([filename, date, date_path])
	print filename