#!/usr/bin/env python

"""
populates a berkelydb rdflib triplestore with triples harvested from 
dewey.info
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

graph.close()
