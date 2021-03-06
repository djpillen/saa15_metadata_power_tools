from lxml import etree
import os
from os.path import join

path = 'demo_eads_normalized'

total_dates = 0
normalized_dates = 0 
non_normalized_dates = 0

for filename in os.listdir(path):	
	tree = etree.parse(join(path,filename))
	unitdates = tree.xpath('//unitdate')
	for unitdate in unitdates:
		if unitdate.text is not None:
			total_dates += 1
			if not 'normal' in unitdate.attrib:
				non_normalized_dates += 1
			else:
				normalized_dates += 1


print "Total dates:", total_dates
print "Normalized dates:", normalized_dates
print "Non-normalized dates:", non_normalized_dates