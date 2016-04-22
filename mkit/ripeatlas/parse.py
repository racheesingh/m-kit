#!/usr/bin/python
import urllib2
import json
import urllib

API_HOST = 'https://atlas.ripe.net'
API_MMT_URI = 'api/v1/measurement'

def mmt_info(msm):
    url = "%s/%s/%d" % (API_HOST, API_MMT_URI, msm)
    try:
        conn = urllib2.urlopen( url )
    except:
        raise ValueError("URL fetch error on: %s" % (url) )
    result = json.load( conn )
    return result

def filter_cruft(data):
    if 'result' in data:
        res = data['result']
        for hop_idx, hop in enumerate( res ):
            if 'result' in hop:
                hop['result'] = [hr for hr in hop['result'] if 'edst' not in hr]
    return data

def parse_msm_trcrt(msm_id, start=None, end=None, count=None):
    '''
    Given a measurement ID from RIPE Atlas, this function fetches the traceroutes
    in the measurement and removes some obvious problems from the data before returning
    it.
    '''
    traceroutes = []
    if not start and not end:
        args = dict(format="txt")
    else:
        args = dict(format="txt", start=start, end=end)

    url_for_msm = "%s/%s/%d/result/?%s" % \
                  (API_HOST, API_MMT_URI, msm_id, urllib.urlencode(args))
    conn = urllib2.urlopen( url_for_msm )
    for dataStr in conn:
        if count:
            if len(traceroutes) > count:
                break
        data = json.loads(dataStr)    
        data = filter_cruft( data )
        if 'result' in data:
            traceroutes.append(data)
    return traceroutes
