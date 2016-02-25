Mkit: Internet Measurement arsenal for data inference and algorithms
====================================================================
Mkit is a consequence of the discussions at the AIMS 2016 organised by CAIDA and [this talk](http://www.caida.org/workshops/aims/1602/slides/aims1602_pgill.pdf) by Dr. Phillipa Gill.
Mkit is a library that facilitates the use of measurement data and provides implementation of common old/new algorithms for Internet measurement data inference.
Mkit would provide the implementation of the common denominator of tasks in terms of the tools the Internet community uses in their everyday work.

As of now, we have APIs for the following:
* RIPE Atlas meta-data (measurement and probes)
* Parsing RIPE traceroute data
* Converting traceroute IP paths to AS paths (naive approach, working towards the one in Sidewalk Ends)
* Handling IXP hops in traceroutes based on from recent [PEERDINGDB](http://docs.peeringdb.com) data.
* Running RIPE measurements (given probes IDs and destination IPs)
* Parsing Iplane traceroutes to AS paths
* CAIDA's pxf2as for IP->ASN mapping
* MMind IP->ASN mapping

But we are actively working towards completing the APIs for parsing other datasets and your help is very welcome!

Common Datasets in Internet Measurement and related sub-domains
===============================================================
While this list is incomplete:

## CAIDA Datasets
* [Prefix to AS](http://data.caida.org/datasets/routing/routeviews-prefix2as/)
* [AS relationships Dataset](http://data.caida.org/datasets/as-relationships/serial-1/)
* [Ark Topology Dataset](http://www.caida.org/data/active/ipv4_routed_24_topology_dataset.xml)

## RIPE Atlas
* [Anchoring Measurements](https://labs.ripe.net/Members/suzanne_taylor_muzzin/announcing-the-ripe-atlas-anchors-service)
* Emile's [Measuring More Internet](https://labs.ripe.net/Members/emileaben/measuring-more-internet-with-ripe-atlas)
* [Probe Meta-datasets](http://ftp.ripe.net/ripe/atlas/probes/archive/2016/)
* All the others available via Mkit or RIPE's own [REST API](https://labs.ripe.net/ripe-database/database-api/api-documentation)

## [Iplane](http://iplane.cs.washington.edu/)
* [PL-PL traceroutes](http://revtr.cs.washington.edu/pl_pl_traceroutes/)
* [Daily traceroutes](http://iplane.cs.washington.edu/data/today/traces_2016_02_23.tar.gz)

## [perfSONAR](http://www.perfsonar.net/about/)
Coming Soon!

## AMP
* All traceroute streams (src, dst): http://www.wand.net.nz/~salcock/amp-traceroute/amp-traceroute.streams.gz

API Features and Design Document (work in progress)
==================================================
[Feature set of Mkit document](https://docs.google.com/document/d/1f0UHg65gaJ_5GElTd3AZWLSEnFNMuliHsm75EOvsa3g/edit?usp=sharing)

## Code Credits
* [Emile Aben](https://github.com/emileaben): much of RIPE Atlas parsing code inspired from [IXP-Country_Jedi](https://github.com/emileaben/ixp-country-jedi)

## Authors
* [Rachee Singh](www.racheesingh.com/about) (SBU)
* [Phillipa Gill](http://www3.cs.stonybrook.edu/~phillipa/) (SBU)
