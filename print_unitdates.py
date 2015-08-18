from lxml import etree
import os
from os.path import join

path = 'demo_eads'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	unitdates = tree.xpath('//unitdate')
	for unitdate in unitdates:
		if unitdate.text is not None:
			print unitdate.text