#!/usr/bin/python
import pygeoip
import constants
import radix

rtree_bgpv4 = radix.Radix()
asn_to_prefs = {}
with open(constants.PFX2ASN_DATA_OLD) as fi:
    for line in fi:
        ip, preflen, asn = line.split()
        if asn in asn_to_prefs:
            asn_to_prefs[asn].append("%s/%s" % (ip, preflen))
        else:
            asn_to_prefs[asn] = ["%s/%s" % (ip, preflen)]
        if ',' in asn:
            tokens = asn.split(',')
            asn = tokens[0]
        if '_' in asn:
            tokens = asn.split('_')
            asn = tokens[0]
        rnode = rtree_bgpv4.add(network=ip, masklen=int(preflen))
        rnode.data["asn"] = asn

rtree_bgpv6 = radix.Radix()
with open(constants.PFX2ASN_DATA_v6) as fi:
    for line in fi:
        ip, preflen, asn = line.split()
        if ',' in asn:
            tokens = asn.split(',')
            asn = tokens[0]
        if '_' in asn:
            tokens = asn.split('_')
            asn = tokens[0]
        rnode = rtree_bgpv6.add(network=ip, masklen=int(preflen))
        rnode.data["asn"] = asn

ai = pygeoip.GeoIP( constants.MAXMIND_DB, pygeoip.MEMORY_CACHE)
def ip2asn_bgp(ip, v6=False):
    if v6:
        try:
            node = rtree_bgpv6.search_best(ip)
        except ValueError:
            print "Could not get AS for IP", ip
            return None
    else:
        try:
            node = rtree_bgpv4.search_best(ip)
        except ValueError:
            print "Could not get AS for IP", ip
            return None
    if node:
        return node.data['asn']
    else:
        return None

def ip2asn_mmind(ip):
    asn = ai.asn_by_addr(ip)
    if asn:
        return str(asn.split()[0].split('AS')[-1])
    else:
        return None

def ip_to_pref(ip):
    try:
        node = rtree_bgpv4.search_best(ip)
    except ValueError:
        print "Could not get AS for IP", ip
        return None

    if node:
        return node
    else:
        return None
