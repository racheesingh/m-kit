import requests
import pdb

r_ixlan = requests.get("https://peeringdb.com/api/ixlan?depth=2")
j_ixlan = r_ixlan.json()

ixplans = {}
for ixlan in j_ixlan['data']:
    ix_id = ixlan['ix_id']
    pfx_set = ixlan['ixpfx_set']
    peeringlans = []
    if len( pfx_set ) == 0:
        continue
    for pe in pfx_set:
        if 'prefix' in pe:
            peeringlans.append( pe['prefix'] )
    if not ix_id in ixplans:
        ixplans[ ix_id ] = []
    ixplans[ ix_id ].append({
        'name': ixlan['name'],
        'desc': ixlan['descr'],
        'peeringlans': peeringlans
    })
        
pdb.set_trace()
