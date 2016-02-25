#!/usr/bin/python

import json
import urllib2

API_HOST = 'https://atlas.ripe.net'
API_MMT_URI = 'api/v1/measurement'

def get_msms(**kwargs)
    data = []

    api_args = dict(kwargs.items())
    url = "%s/%s/?%s" % ( API_HOST, API_MMT_URI, urllib.urlencode(api_args))
    response = urllib2.urlopen( url )
    data = json.load( response )
    if not data[ 'objects' ]:
        return []
    else:
        return data['objects']


