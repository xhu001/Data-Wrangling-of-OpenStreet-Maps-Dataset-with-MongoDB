#CODE 4
# check street name ab.
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "harrisburg_pennsylvania.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)#search to see if street_name is in 

    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)



def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    #osm_file = open(osmfile, "r")
    street_types = defaultdict(set)# this dict has value with default type of set
    for _, elem in ET.iterparse(OSMFILE):
         for tag in elem.iter("tag"):
            if is_street_name(tag):
                 audit_street_type(street_types, tag.attrib['v'])

    return street_types


def test():
    st_types = audit(OSMFILE)

    pprint.pprint(dict(st_types))

if __name__ == '__main__':
    test()
