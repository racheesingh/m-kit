#!/usr/bin/python
from random import shuffle
import random
import os
import pp
import sys
from datetime import datetime
from radix import Radix
import json
import ripe.atlas.sagan
import pycountry
from ripe.atlas.cousteau import ProbeRequest
import subprocess
import pdb
from Atlas import Measure
from Atlas import MeasurementFetch
from Atlas import MeasurementInfo
from Atlas import MeasurementPrint
from Atlas import MeasurementEnhance
import time

#ATLAS_API_KEY = "5f35d4a7-b7d3-4ab8-b519-4fb18ebd2ead"
ATLAS_API_KEY = "ec028142-a67b-4c73-a7e0-e4c1a6ef7fa9" # my own key

now = '-'.join( str( datetime.now() ).split() )
DEFAULT_NUM_PROBES = 5
country_name = sys.argv[ 1 ].lower()
if len( sys.argv ) < 3:
        num_probes = DEFAULT_NUM_PROBES
else:
    num_probes = int( sys.argv[ 2 ] )

country_list = list(pycountry.countries)
country_dict = dict( ( x.name, x.alpha2 ) for x in country_list )
def get_country_code( country_name ):
    if country_name in country_dict:
        return country_dict[ country_name ]
    country_code = [ country_dict[ key ] for key in country_dict.keys()
                     if country_name.lower() in key.lower() ][ 0 ]
    return country_code

def get_asn_list( country_name ):
    country_code = get_country_code( country_name )
    output = subprocess.check_output(
        "curl www.cc2asn.com/data/%s_asn" % country_code.lower(), shell=True )
    return [ asn for asn in output.split( '\n' ) if asn ]

def get_probes( country_name ):
    country_code = get_country_code( country_name )
    filters = { "country_code": country_code }
    probes = ProbeRequest( **filters )
    probe_list = []
    for p in probes:
        if 'address_v4' in p and p['address_v4'] and \
           'system-ipv4-works' in p['tags']:
            probe_list.append( p )
    return probe_list

''' Will collect all probes in all countries
except the ones in the country we are measuring'''
def get_random_probes():
    probes = []
    countries = country_dict.keys()
    while( len(probes) < num_probes ):
        name = random.choice( countries )
        pr = get_probes( name )
        if pr:
            shuffle( pr )
            probes.append( pr[0] )
    assert len(probes) == num_probes
    return probes

def run_measurement():
    msms_in = []
    msms_out = []
    intl_probes = get_random_probes()
    intl_src_probes = [ x[ 'id' ] for x in intl_probes ]
    intl_dst_probes = [ x[ 'address_v4' ] for x in intl_probes ]
    dom_probes = get_probes( country_name )
    shuffle( dom_probes )
    dom_probes = dom_probes[ :num_probes ]
    if not dom_probes:
        print "No probes in %s" % country_name
        return
    if not intl_probes:
        print "Something wrong with probe selection, no international probes found"
        return
    dom_src_probes = [ x[ 'id' ] for x in dom_probes ]
    dom_dst_probes = [ x[ 'address_v4' ] for x in dom_probes ]
    print "Tracerouting to %s from outside.." % country_name
    for dest in dom_dst_probes:
        try:
            msm_id = Measure.oneofftrace(
                intl_src_probes, dest, af=4, paris=1,
                description="ASN graph for %s: testing traceroute to %s" % ( country_name, dest ) )
            if msm_id:
                msms_in.append( msm_id )
                sleep(2)
        except:
            time.sleep( 100 )
            pdb.set_trace()
            pass
    print "Tracerouting from %s to outside.." % country_name
    for dest in intl_dst_probes:
        try:
            msm_id = Measure.oneofftrace(
                dom_src_probes, dest, af=4, paris=1,
                description="ASN graph for %s: testing traceroute to %s" % ( country_name, dest ) )
            if msm_id:
                msms_out.append( msm_id )
        except:
            time.sleep( 100 )
            pdb.set_trace()
            pass
    return { 'in': msms_in, 'out': msms_out }

msms = run_measurement()

if msms:
    if not os.path.isdir( country_name ):
        os.makedirs( country_name )
    mmtfile = "%s/%s-%s.json" % ( country_name, country_name, now )
    with open( mmtfile, "w" ) as f:
        json.dump( msms, f )
