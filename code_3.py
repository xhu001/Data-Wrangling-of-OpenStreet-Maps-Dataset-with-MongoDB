#CODE 3
# Convert XML to JSON amd correct street abr.
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict
 

def update_address_name(name):
    street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
    mapping = { "St.": "Street",
            "Rd.": "Road",
            "Dr":"Drive",
            "Blvd.":"Boulevard "
            }
    m = street_type_re.search(name)    
    if mapping.get(m.group()):
        name = name.replace(m.group(),mapping[m.group()])
    return name  


def shape_element(element): #xml2Json

    node = {}
    created = {}
    addr_like = []
    temp =[]
    refs = []
    members = []
    new_format = defaultdict(dict)
    pos = []

    created["version"] = element.attrib.get("version",None) 
    created["changeset"] = element.attrib.get("changeset",None)  
    created["timestamp"] = element.attrib.get("timestamp",None)        
    created["user"] = element.attrib.get("user",None)        
    created["uid"] = element.attrib.get("uid",None)        
    node["record_id"] = element.attrib.get("id",None)       
    node["visible"] = element.attrib.get("visible",None)                           
    node["record_type"] = element.tag
    node["record_created"] = created
    pos.append(float_num(element.attrib.get("lat",None)))
    pos.append(float_num(element.attrib.get("lon",None)))
    node['pos'] = pos
    for children in element.iter():
        if (children.tag == 'tag'):
            cut_here = children.get('k').find(':')# for ####:$$$$
            if (cut_here > 0):
                temp.append(children.get('k')[0:cut_here])     #[0] is the name used for dictionary
                temp.append(children.get('k')[cut_here+1:])    #[1] new key
                if children.get('k').find('addr:street') != -1:# correct street ab.
                    temp.append(update_address_name(children.get('v')))
                else:
                    temp.append(children.get('v'))              #[2] value
                addr_like.append(temp)
                temp = []
            else:
                node[children.get('k')] = children.get('v')     
        elif (children.tag == 'nd'):  
                refs.append(children.get('ref'))
        elif (children.tag =='member'):    
                mem_tmp = {}
                mem_tmp['type'] = children.get('type')
                mem_tmp['ref'] = children.get('ref')
                mem_tmp['role'] = children.get('role') 
                members.append(mem_tmp)
                

    if len(addr_like) > 0:  
        for keys, sub_key, values in addr_like:#for ####:$$$$, to dictionary
            tmp ={}
            tmp[sub_key] = values
            new_format[keys].update(tmp)
        node.update(new_format)
        if node.get('tiger'):#zipcode
            node['zip'] = (node['tiger'].get('zip_left'))

    if len(refs) > 0:
        node['refs'] = refs
        refs = []

    if len(members) > 0:
        node['members'] = members
        members = []

    return node
    

def float_num(my_str):
    if my_str != None:
        try:
            return float(my_str)
        except ValueError:
            return None
    return None
    
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            if element.tag == "node" or element.tag == "way" or element.tag == "relation":
                el = shape_element(element)
                if el:
                    data.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
        return data

def test():

    data = process_map('harrisburg_pennsylvania.osm', False)
    print ("All Done!")

if __name__ == "__main__":
    test()
