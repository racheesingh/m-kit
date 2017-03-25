import getpass
user = getpass.getuser()

PFX2ASN_DATA = "/home/%s/data/routeviews-rv2-20170107-1200.pfx2as" % user
MAXMIND_DB = "/home/%s/data/GeoIPASNum.dat" % user
IXP_DATA_PEERINGDB = "/home/%s/data/peeringdb-ixps.txt" % user
IXP_ALL = "/home/%s/data/all_ixps.csv" % user
