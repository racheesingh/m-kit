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
    
all_probes = init_probset()
probes_by_id = {}
for pr in all_probes:
    probes_by_id[pr['prb_id']] = pr
    