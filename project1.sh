#!/bin/bash

# Kathryn Nichols
# Stefan Behr
# LING 571
# Project 1

# This shell script uses convert_grammar.py and parse.py to 
# convert a CFG to CNF, and then use that grammar in conjunction 
# with a CKY parser implementation to parse a set of sentences in 
# a file at a provided pathname argument.

python2.7 convert_grammar.py $1 $2 # convert grammar at first path arg to CNF form saved at second path arg
python2.7 parse.py $3 $2 # parse sentences at third path arg using a parser and grammar which was saved to second path arg