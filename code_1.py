# CODE 1
# count tags and attributes.

import xml.etree.cElementTree as ET
import pprint
import re


def iter_count_tags(filename):
    tree = ET.iterparse(filename)#get content
    counts = []
    tags = {}#tag
    k = {}#attribute
    
    for event, elem in tree: 
        if  not (elem.tag in tags.keys()):
            tags[elem.tag] = 1
            for key in elem.attrib.keys():
                if not (key in k.keys()):
                    k[key] = 1
                else:
                    k[key] += 1
        else:
            tags[elem.tag] = tags[elem.tag] + 1
            for key in elem.attrib.keys():
                if not (key in k.keys()):
                    k[key] = 1
                else:
                    k[key] += 1
    counts.append(tags)
    counts.append(k)
    
    return counts

def test():
    
    counts = iter_count_tags('harrisburg_pennsylvania.osm')
    pprint.pprint(counts)

    

if __name__ == "__main__":
    test()
