# CODE 2
# count value of 'k'

import xml.etree.cElementTree as ET
import pprint
import sys
import re


def iter_count_tags(filename):
    tree = ET.iterparse(filename)#get content
    tag_k_value = {}#tag
  
    
    for event, elem in tree: 
        if  elem.tag == 'tag':
            value = elem.attrib['k']
            if not (value in tag_k_value.keys()):
                tag_k_value[value] = 1
            else:
                 tag_k_value[value] += 1
    
    return tag_k_value

def test():
    
    counts = iter_count_tags('harrisburg_pennsylvania.osm')
    pprint.pprint(counts)

    

if __name__ == "__main__":
    test()
