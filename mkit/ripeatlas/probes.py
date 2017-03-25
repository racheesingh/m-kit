#!/usr/bin/python
import constants
import json

def init_probset():
    with open(constants.RIPE_PROBE_DATA) as fd:
        jsonStr = json.load(fd)

    total_count = jsonStr['meta']['total_count']
    all_probes = []
    for probeCount in range(total_count):
        probe = jsonStr['objects'][probeCount]
        all_probes.append(probe)
    return all_probes

def get_all_ipv4():
    candidate_set = []
    for pr in all_probes:
        if 'system-ipv4-works' in pr['tags'] and pr['status_name'] == 'Connected':
            candidate_set.append(pr)
    return candidate_set

def get_all_ipv6():
    candidate_set = []
    for pr in all_probes:
        if 'system-ipv6-works' in pr['tags'] and pr['status_name'] == 'Connected':
            candidate_set.append(pr)
    return candidate_set

def get_probes_in_asn(asn):
    asn = int(asn)
    candidate_set = []
    for pr in all_probes:
        if 'system-ipv6-works' in pr['tags'] and pr['status_name'] == 'Connected':
            if pr['asn_v4'] == asn:
                candidate_set.append(pr)
    return candidate_set

def get_probes_in_country(iso_country_code):
    candidate_set = []
    for pr in all_probes:
        if 'system-ipv6-works' in pr['tags'] and pr['status_name'] == 'Connected':
            if pr['country_code'] == iso_country_code:
                candidate_set.append(pr)
    return candidate_set

def get_probe_asn(prb_id):
    if prb_id not in probes_by_id:
        print "Incorrect probe ID!"
        return None
    return probes_by_id[prb_id]['asn_v4']

def get_probe_spread():
    customer_cones = {}
    with open(constants.CAIDA_CUST_CONE) as fi:
        for line in fi:
            if line.startswith('#'): continue
            asn_list = line.split()
            if len(asn_list) > 1:
                try:
                    customer_cones[int(asn_list[0])] = len([int(x) for x in asn_list[1:]])
                except:
                    continue

    probes_per_asn = {}
    for pr in all_probes:
        if 'system-ipv6-works' in pr['tags'] and pr['status_name'] == 'Connected':
            asn = pr['asn_v4']
            if not asn: continue
            if asn in probes_per_asn:
                probes_per_asn[int(asn)] += 1
            else:
                probes_per_asn[int(asn)] = 1
    per_asn_cone_probes = {}
    for asn in probes_per_asn:
        if asn in customer_cones:
            per_asn_cone_probes[asn] = (probes_per_asn[asn], customer_cones[asn])
        else:
            per_asn_cone_probes[asn] = (probes_per_asn[asn], 0)
    return per_asn_cone_probes
    
all_probes = init_probset()
probes_by_id = {}
for pr in all_probes:
    probes_by_id[pr['id']] = pr
    
