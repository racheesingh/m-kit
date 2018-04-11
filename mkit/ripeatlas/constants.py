import getpass
user = getpass.getuser()
DATA_DIR = "/home/%s/data" % user
RIPE_PROBE_DATA = "/home/%s/data/20180218.json" % user
CAIDA_CUST_CONE = "/home/%s/data/20161101.ppdc-ases.txt" % user
