import csv
from lxml import etree
from os.path import join

path = 'demo_eads_normalized'

with open('normalized_dates.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        filename = row[0]
        print filename
        xpath = row[1]
        normalized = row[3]
        ead_file = open(join(path, filename))
        tree = etree.parse(ead_file)
        unitdate = tree.xpath(xpath)
        unitdate[0].attrib['normal'] = normalized
        outfile = open(join(path, filename), 'w')
        outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
        outfile.close()

print "Normalization Complete"
