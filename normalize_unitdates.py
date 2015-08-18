# Normalize unitdates that are a a year or a range of years

# import what we need
from lxml import etree
import os
from os.path import join
import re


path = 'demo_eads' #<-- Change this to your EAD directory path

# Make some regular expressions
yyyy = re.compile(r'^\d{4}$') # Ex: 1920
yyyys = re.compile(r'^\d{4}s$') # Ex: 1920s
yyyy_yyyy = re.compile(r'^\d{4}\-\d{4}$') # Ex: 1920-1930
yyyys_yyyy = re.compile(r'^\d{4}s\-\d{4}$') # Ex: 1920s-1930
yyyy_yyyys = re.compile(r'^\d{4}\-\d{4}s$') # Ex: 1920-1930s
yyyys_yyyys = re.compile(r'^\d{4}s\-\d{4}s$') # Ex: 1920s-1930s

# Initialize these values to keep track of how many dates we've normalized
total_dates = 0
normalized_dates = 0
not_normalized_dates = 0

for filename in os.listdir(path):
    print filename # Print the filename that is currently being checked. This is helpful for identifying errors.
    tree = etree.parse(join(path, filename))
    # xpath that checks for a <unitdate> anywhere in the EAD
    unitdates = tree.xpath('//unitdate')
    # loop through each <unitdate>
    for unitdate in unitdates:
        if unitdate.text is not None:
            total_dates += 1
            if not 'normal' in unitdate.attrib:
                # check if the content of <unitdate> matches any of those regular expressions
                if yyyy.match(unitdate.text) and len(unitdate.text) == 4: # We also verify that the length is what we would expect based on the regular expression for an added level of certainty that these really are the kinds of dates we're looking for
                    unitdate.attrib['normal'] = unitdate.text # Dates like "1920" don't need to be changed at all to make a normalized version
                    normalized_dates += 1
                elif yyyys.match(unitdate.text) and len(unitdate.text) == 5:
                    unitdate.attrib['normal'] = unitdate.text.replace('s', '') + '/' + unitdate.text[:3] + '9' # Change dates like "1920s" to "1920/1929"
                    unitdate.attrib['certainty'] = "approximate" # Since this is a date range and not an exact date, add an "approximate" certainty attribute
                    normalized_dates += 1
                elif yyyy_yyyy.match(unitdate.text) and len(unitdate.text) == 9:
                    unitdate.attrib['normal'] = unitdate.text.replace('-', '/') # Dates like "1920-1930" are easy: simply replae the '-' with a '/' to get "1920/1930"
                    normalized_dates += 1
                elif yyyys_yyyy.match(unitdate.text) and len(unitdate.text) == 10:
                    unitdate.attrib['normal'] = unitdate.text.replace('-', '/').replace('s', '') # "1920s-1930" becomes "1920/1930" by dropping the 's' and changing the '-' to a '/'
                    unitdate.attrib['certainty'] = "approximate"
                    normalized_dates += 1
                elif yyyy_yyyys.match(unitdate.text) and len(unitdate.text) == 10:
                    normalized = unitdate.text.replace('-', '/') # For dates like "1920-1930s", first replace the '-' with a '/' to get "1920/1930s"
                    normalized = normalized.replace(normalized[-2:], '9') # Now replace the last two characters with '9', yielding "1920/1939"
                    unitdate.attrib['normal'] = normalized
                    unitdate.attrib['certainty'] = "approximate"
                    normalized_dates += 1
                elif yyyys_yyyys.match(unitdate.text) and len(unitdate.text) == 11:
                    normalized = unitdate.text.replace('-', '/').replace('s', '', 1) # For dates like "1920s-1930s', replace the '-' with a '/' and remove ONLY the first 's' to get "1920/1930s"
                    normalized = normalized.replace(normalized[-2:], '9') # Now replace the last to characters with '9', yielding "1920/1939"
                    unitdate.attrib['normal'] = normalized
                    unitdate.attrib['certainty'] = "approximate"
                    normalized_dates += 1
                else:
                    continue

    outfilepath = 'demo_eads_normalized' #<-- Change this to a different directory than the one you started with in case anything goes wrong. You don't want to overwrite your original EADs.
    outfile = open((join(outfilepath, filename)), 'w')
    outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True)) # Write the new version of the EAD with normalized dates!
    outfile.close()

# Print the results of our normalization attempt
print "Normalization attempted on " + str(total_dates) + " dates"
print "Number of dates normalized: " + str(normalized_dates)
print "Number of dates not normalized: " + str(total_dates - normalized_dates)