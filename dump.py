#!/usr/bin/env python

import json
import rdflib
from rdflib.namespace import RDF

g = rdflib.ConjunctiveGraph('Sleepycat')
g.open('store')

g.bind('cc', 'http://creativecommons.org/ns#')
g.bind('dcterms', 'http://purl.org/dc/terms/')
g.bind('xhtml', 'http://www.w3.org/1999/xhtml/vocab#')
g.bind('skos', 'http://www.w3.org/2004/02/skos/core#')

# dump turtle/n3
g.serialize(open('dewey.ttl', 'w'), format='n3')

# dump rdf/xml
g.serialize(open('dewey.rdf', 'w'), format='xml')

# dump json
skos = rdflib.Namespace('http://www.w3.org/2004/02/skos/core#')
dct = rdflib.Namespace('http://purl.org/dc/terms/')

dcc = {}
for concept in g.subjects(RDF.type, skos.Concept):
    code = unicode(g.value(concept, skos.notation)).replace('[]', '')
    label = g.value(concept, skos.prefLabel)
    if not dcc.has_key(code):
        dcc[code] = {}
    dcc[code][label.language] = unicode(label)

open('dewey.json', 'w').write(json.dumps(dcc, indent=2))
g.close()
