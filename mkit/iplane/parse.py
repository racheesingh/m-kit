#!/usr/bin/python
from networkx.readwrite import json_graph
import json
import sys
import traceback
from itertools import groupby
import multiprocessing as mp
import networkx as nx
import pdb
import re
import os
from datetime import datetime, timedelta
from ..inference import ip_to_asn as ip2asn
import constants
from ..inference import ixp as ixp

print "To ensure correct usage, place the extracted Iplane dumps (get from here: http://iplane.cs.washington.edu/data/today/traces_2016_02_27.tar.gz) in ~/data/iplane/. Place the readout file (http://iplane.cs.washington.edu/data/readoutfile) in ~/data/iplane/ and then the APIs will be able to find the data."

def parse_iplane_file(dirName, fName):
    print "Parsing file", fName
    as_paths_dict = {}
    aspath = []
    current_dest = None
    ipRegex = r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))"
    parseCommand = "%s %s > %s" % (constants.readOutExec, fName, fName+"-read")
    os.system(parseCommand)
    with open(fName+"-read") as fi:
        for line in fi:
            if 'destination' in line:
                match = re.search(ipRegex, line)
                if match:
                    # Add previous AS path to dictionary
                    if current_dest and aspath and current_dest in as_paths_dict:
                        as_paths_dict[(current_dest, dst_prefix)].append(aspath)
                    elif current_dest and aspath:
                        as_paths_dict[(current_dest, dst_prefix)] = [aspath]
                    dest = match.group(0)
                    ixp_match = ixp.ixp_radix.search_best(dest)
                    if ixp_match:
                        continue
                    rnode = ip2asn.ip_to_pref(dest)
                    asn = ip2asn.ip2asn_bgp(dest)
                    if asn and rnode:
                        if asn in ixp.IXPs:
                            continue
                        aspath = []
                        current_dest = asn
                        current_hop_nr = None
                        last_hop_nr = None
                        current_asn = None
                        prev_asn = None
                        dst_prefix = rnode.prefix.replace('/', '_')
            elif current_dest:
                last_hop_nr = current_hop_nr
                prev_asn = current_asn

                # If current destination is not set, what could we even gather a path towards?
                match = re.search(ipRegex, line)
                if match:
                    hop = match.group(0)
                    ixp_match = ixp.ixp_radix.search_best(hop)
                    if ixp_match:
                        continue
                    asn = ip2asn.ip2asn_bgp(hop)
                    if asn:
                        if asn in ixp.IXPs:
                            continue
                        current_asn = asn
                        current_hop_nr = int(line.split(':')[0])
                        if prev_asn and current_asn and prev_asn != current_asn:
                            if current_hop_nr - last_hop_nr == 1:
                                linktype = 'd'
                            else:
                                linktype = 'i'
                            link = (int(prev_asn), int(current_asn), linktype)
                            aspath.append(link)
    return as_paths_dict

def get_iplane_graphs(dates):
    dir_files = {}
    for date in [dates]:
        dirName = "traces_" + date 
        dir_path = os.path.join(constants.IPLANE_DATA, dirName)
        files = [x for x in os.listdir(dir_path) if
                 os.path.isfile(os.path.join(dir_path, x))]
        files = [os.path.join(dir_path, f) for f in files]
        dir_files[ dirName ] = files
    
    results = []
    pool = mp.Pool(processes=32)
    for dName, files in dir_files.iteritems():
        for f in files:
            results.append( pool.apply_async( parse_iplane_file, args=(dName,f) ) )
            #parse_iplane_file(dName, f)

    pool.close()
    pool.join()
    output = [ p.get() for p in results ]
    dest_based_as_paths = {}
    for op in output:
        for tup, aspaths in op.iteritems():
            dst_asn = tup[0]
            if not dst_asn in dest_based_as_paths:
                dest_based_as_paths[dst_asn] = aspaths
            else:
                dest_based_as_paths[dst_asn].extend(aspaths)
    return dest_based_as_paths


def get_iplane_prefix_graphs(dates):
    dir_files = {}
    for date in [dates]:
        dirName = "traces_" + date 
        dir_path = os.path.join(constants.IPLANE_DATA, dirName)
        files = [x for x in os.listdir(dir_path) if
                 os.path.isfile(os.path.join(dir_path, x))]
        files = [os.path.join(dir_path, f) for f in files]
        dir_files[ dirName ] = files
    
    results = []
    pool = mp.Pool(processes=32)
    for dName, files in dir_files.iteritems():
        for f in files:
            results.append( pool.apply_async( parse_iplane_file, args=(dName,f) ) )
            #parse_iplane_file(dName, f)

    pool.close()
    pool.join()
    output = [ p.get() for p in results ]
    dest_based_as_paths = {}
    for op in output:
        for tup, aspaths in op.iteritems():
            dst_prefix = tup[1]
            if not tup in dest_based_as_paths:
                dest_based_as_paths[tup] = aspaths
            else:
                dest_based_as_paths[tup].extend(aspaths)
    return dest_based_as_paths


