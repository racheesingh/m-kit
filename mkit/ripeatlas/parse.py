#!/usr/bin/python
import urllib2
import json
import urllib

API_HOST = 'https://atlas.ripe.net'
API_MMT_URI = 'api/v1/measurement'

def filter_cruft( data ):
    if 'result' in data:
        res = data['result']
        for hop_idx, hop in enumerate( res ):
            if 'result' in hop:
                hop['result'] = [hr for hr in hop['result'] if 'edst' not in hr]
    return data

def parse_msm_trcrt(msm_id):
    '''
    Given a measurement ID from RIPE Atlas, this function fetches the traceroutes
    in the measurement and removes some obvious problems from the data before returning
    it.
    '''
    traceroutes = []
    url_for_msm = "%s/%s/%d/result/?%s" % \
                  (API_HOST, API_MMT_URI, msm_id, urllib.urlencode(dict({'format': 'txt'})))
    conn = urllib2.urlopen( url_for_msm )
    for dataStr in conn:
        data = json.loads(dataStr)    
        data = filter_cruft( data )
        if 'result' in data:
            traceroutes.append(data)
    return traceroutes
