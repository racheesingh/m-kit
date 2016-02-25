Mkit: Internet Measurement arsenal for data inference and algorithms

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