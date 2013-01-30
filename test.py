#!/usr/bin/env python2.7

import nltk
from parser import CKYParser

p = CKYParser("grammar.cnf")
s = nltk.wordpunct_tokenize("Before the discovery of DNA heredity was a mystery.")

parses = p.get_parses(s)

print "\n".join(parses)
print len(parses)
