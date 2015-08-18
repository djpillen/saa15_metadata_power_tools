import csv
from lxml import etree
import os
from os.path import join

path = 'demo_eads'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	unitdates = tree.xpath('//unitdate')
	for unitdate in unitdates:
		if unitdate.text is not None:
			date = unitdate.text
			date_path = tree.getpath(unitdate)
			with open('all_unitdates.csv','ab') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow([filename, date, date_path])
	print filename