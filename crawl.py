#!/usr/bin/env python

"""
Simplistic single-threaded crawler for linked data at http://dewey.info/

You'll need to have rdflib installed <http://rdflib.net>, afterwhich you
should be able to run: crawl.py

After a successful run you should have a dewey.rdf and dewey.ttl file in 
your working directory.
"""

import rdflib

def crawl(uri):
    g = rdflib.ConjunctiveGraph()
    g.load(uri)

    for s in g.subjects():
        if not s in seen:
            seen.add(s)
            uris.append(s)

    for o in g.objects():
        if isinstance(o, rdflib.URIRef) and not o in seen:
            seen.add(o)
            uris.append(o)

    for t in g:
        graph.add(t)

seen = set()
uris = ['http://dewey.info/class/%s/' % n for n in range(0,10)]
graph = rdflib.ConjunctiveGraph('Sleepycat')
graph.open('store', create=True)

while len(uris) > 0:
    uri = uris.pop(0)

    if 'http://dewey.info' not in uri: 
        print "skipping: %s" % uri
        continue
    try:
        print "crawling: %s" % uri
        crawl(uri)
    except KeyboardInterrupt:
        break
    except Exception, e:
        print e

graph.bind('cc', 'http://creativecommons.org/ns#')
graph.bind('dcterms', 'http://purl.org/dc/terms/')
graph.bind('xhtml', 'http://www.w3.org/1999/xhtml/vocab#')
graph.bind('skos', 'http://www.w3.org/2004/02/skos/core#')
graph.serialize(open('dewey.ttl', 'w'), format='n3')
graph.serialize(open('dewey.rdf', 'w'), format='xml')

graph.close()
