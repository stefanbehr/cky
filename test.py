#!/usr/bin/env python2.7

import nltk
from parser import CKYParser

p = CKYParser("grammar.cnf")
s = nltk.wordpunct_tokenize("Before the discovery of DNA heredity was a mystery.")

p.parse(s)

for parse in p.chart[0][len(s)]:
    print parse.symbol
    if parse.left:
        print ":", parse.left.symbol
    if parse.right:
        print ":", parse.right.symbol
    
