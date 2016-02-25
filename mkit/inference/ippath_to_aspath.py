#!/usr/bin/python
import constants
import pdb
import ip_to_asn as ip2asn
import ixp

ixp_radix = ixp.ixp_radix

def getlinktype( numASHop1, numASHop2 ):
    if numASHop2 - numASHop1 > 1:
        return 'i'
    return 'd'

def traceroute_to_aspath(data, src_asn):
    aslinks = {'_nodes': set(), '_links': [] }
    if 'result' in data:
        res = data['result']
        last_resp_hop_nr = None
        last_resp_hop_ases = set()
        this_hop_ases = None

        for hop in res:
            if 'hop' not in hop:
                print "No hop info in", hop
                    
            if this_hop_ases and len(this_hop_ases) > 0:
                last_resp_hop_ases = this_hop_ases
                last_resp_hop_nr = this_resp_hop_nr
                    
            this_resp_hop_nr = hop['hop']
            ips = set()
            if 'result' in hop:
                for hr in hop['result']:
                    if 'from' in hr:
                        if hr['from'] not in ips:
                            ips.add(hr['from'])
            this_hop_ases = set()
            for ip in ips:
                asn = ip2asn.ip2asn_bgp(ip)
                this_hop_ases.add(asn)
                        
            if len(this_hop_ases) == 1 and len(last_resp_hop_ases) == 1:
                this_asn = list(this_hop_ases)[0]
                last_asn = list(last_resp_hop_ases)[0]
                if this_asn != last_asn:
                    ixps = [ixp_radix.search_best(x) for x in ips]
                    if any(ixps):
                        continue
                    link_type = getlinktype(last_resp_hop_nr, this_resp_hop_nr)
                    link = { 'src': last_asn,
                             'dst': this_asn, 'type': link_type }
                    aslinks['_nodes'].add( this_asn )
                    aslinks['_nodes'].add( last_asn )
                    aslinks['_links'].append( link )

            elif len(this_hop_ases) == 0 or len(last_resp_hop_ases) == 0:
                pass # uninteresting
            else:
                # Difference ASes at a hop, ignoring such traceroutes
                print "Uncaught situation at hop no %s->%s: %s->: %s" % \
                    ( last_resp_hop_nr, this_resp_hop_nr , last_resp_hop_ases, this_hop_ases )
                continue
                    
    if not aslinks['_links']:
        return aslinks
    
    # Many times, the first hop address is a local (non-routable) prefix, so
    # prepending src_asn to the AS level path since we know for sure that the traceroute
    # originated from src_asn
    if aslinks['_links'][0]['src'] != str(src_asn):
        aslinks['_links'] = [{'src':src_asn, 'dst':aslinks['_links'][0]['src'], 'type':'i'}] + \
                            aslinks['_links']
    
    # This code block short circuits paths like A->B->C->B->D to A->B->D
    # Also A->B->A->C->D should become A->C->D.
    linkssane = []
    delnext = False
    for index in range(len(aslinks['_links'])):
        if delnext:
            delnext = False
            continue
    if (index + 1) < len(aslinks['_links']):
        if aslinks['_links'][index]['src'] == aslinks['_links'][index+1]['dst']:
            delnext = True
        else:
            linkssane.append(aslinks['_links'][index])
    else:
        linkssane.append(aslinks['_links'][index])
            
    loopdetect = []
    for link in linkssane:
        loopdetect.append(link['src'])
    loopdetect.append(link['dst'])
    loops = [i for i,x in enumerate(loopdetect) if loopdetect.count(x) > 1]
    if loops:
        # Cannot trust this traceroute, it has loops
        aslinks['_links'] = []
        return aslinks
    
    aslinks['_links'] = linkssane
    return aslinks

