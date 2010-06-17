#!/usr/bin/env python

"""
Simplistic cralwer for rdfa linked data at dewey.info.
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
uris = ['http://dewey.info/class/00/2009/08/about.en']
graph = rdflib.ConjunctiveGraph('Sleepycat')
graph.open('store', create=True)

while len(uris) > 0:
    uri = uris.pop(0)
    print uri

    if 'http://dewey.info' not in uri: 
        print "skipping: %s" % uri
        continue
    try:
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

graph.close()
