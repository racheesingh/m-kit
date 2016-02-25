Mkit: Internet Measurement arsenal for data inference and algorithms
====================================================================

Mkit is a library that facilitates the use of measurement data and provides implementation of old/new algorithms for data inference.
M-kit would provide the implementation of the common denominator in terms of the tools the Internet community uses in their everyday work.
As of now, we have APIs for the following:
* RIPE Atlas meta-data (measurement and probes)
* Parsing RIPE traceroute data
* Converting traceroute IP paths to AS paths (naive approach, working towards the one in Sidewalk Ends)
* Handling IXP hops in traceroutes based on from recent PEERDINGDB data.
* Running RIPE measurements (given probes IDs and destination IPs)
* Parsing Iplane traceroutes to AS paths
* CAIDA's pxf2as for IP->ASN mapping
* MMind IP->ASN mapping

But we are actively working towards completing the APIs for parsing other datasets and your help is very welcome!

Common Datasets in Internet Measurement and related sub-domains
===============================================================
While this list is incomplete:

CAIDA Datasets:
1. [Prefix to AS](http://data.caida.org/datasets/routing/routeviews-prefix2as/)
2. [AS relationships Dataset](http://data.caida.org/datasets/as-relationships/serial-1/)
3. [Ark Topology Dataset](http://www.caida.org/data/active/ipv4_routed_24_topology_dataset.xml)

RIPE Atlas:
1. [Anchoring Measurements](https://labs.ripe.net/Members/suzanne_taylor_muzzin/announcing-the-ripe-atlas-anchors-service)
2. Emile's [Measuring More Internet](https://labs.ripe.net/Members/emileaben/measuring-more-internet-with-ripe-atlas)
3. All the others available via Mkit or RIPE's own [REST API](https://labs.ripe.net/ripe-database/database-api/api-documentation)

Iplane:
1. [PL-PL traceroutes](http://revtr.cs.washington.edu/pl_pl_traceroutes/)
2. [Daily traceroutes](http://iplane.cs.washington.edu/data/today/traces_2016_02_23.tar.gz)

perfSONAR:

AMP:
1. All traceroute streams (src, dst): http://www.wand.net.nz/~salcock/amp-traceroute/amp-traceroute.streams.gz