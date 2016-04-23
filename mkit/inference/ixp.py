#!/usr/bin/python
import pdb
import constants
import radix

# List of IXP ASNs
IXPs = [ '1200',  '4635',  '5507', '6695', '7606', '8714', '9355', '9439', '9560',
         '9722', '9989', '11670', '17819', '18398', '21371', '24029', '24115',
         '24990', '35054', '40633', '42476', '43100', '47886', '48850', '55818' ]

def remove_ixps(data):
    nodes = data['_nodes']
    links = data['_links']
    # First node is an IXP (don't know how and why), cut that edge out
    if links[0]['src'] in IXPs:
        nodes.remove(links[0]['src'])
        links = links[1:]
    if set( nodes ).isdisjoint(set(IXPs)):
        return links
        
    ixps = list(set(IXPs).intersection(set(nodes)))
    new_links = []
    connecting_link = {}
    for link in links:
        if 'src' in connecting_link and 'dst' in connecting_link:
            connecting_link['type'] = 'i'
            new_links.append(connecting_link)
            connecting_link = {}
        if link['dst'] in ixps:
            assert 'src' not in connecting_link
            connecting_link['src'] = link['src']
        elif link['src'] in ixps:
            assert 'dst' not in connecting_link
            connecting_link['dst'] = link['dst']
        else:
            new_links.append(link)
    return new_links

ixp_radix = radix.Radix()
with open(constants.IXP_DATA_PEERINGDB) as fi:
    for line in fi:
        tokens = line.split('\t')
        if ':' in tokens[-1]:
            continue
        node = ixp_radix.add(tokens[-1].split('\n')[0])
        node.data["name"] = tokens[0]
