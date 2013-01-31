# -*- coding: utf-8 -*-
"""
Kathryn Nichols
Stefan Behr
LING 571
Project 1

This program reads in a context free grammar at arg 1 and outputs the 
grammar in Chomsky Normal Form to the file at arg 2. Comments and empty
lines are eliminated from the file. Assumes the form of the input is 
line-delimited rules, with LHS and RHS separated by ->, and multiple RHS 
productions separated by | . Terminals should be denoted with straight 
apostrophes on either side. Each line of comment should be preceded
by #. The first LHS symbol in the file is treated as the initial symbol.
Input that does not follow this format may fail to output an
equivalent CNF file.

"""

import sys

rule_map = {}       # stores rules

# Returns a list of terminals and their
# indices in the given rule
def find_terminals(rule):
    terminals = []
    indices = []
    j = 0
    for item in rule:
        if item[0] == "'":
            terminals.append(item)
            indices.append(j)
        j += 1
    
    return terminals, indices

# Returns a string representation
# of the given rule
def stringify(rule):
    string = rule[0] + ' ->'
    for item in rule[1:]:
        string += ' ' + item
    string += '\n'
    
    return string

# Adds a rule to the dictionary of rules
def add_rule(rule):
    
    global rule_map
    
    if rule[0] not in rule_map:
        rule_map[rule[0]] = []
    rule_map[rule[0]].append(rule[1:])

# Replaces the terminals in the given
# rule with new nonterminals. Adds
# new rules to the output, returns
# altered rule
def replace_terminals(rule, terminals, indices, i):
    
    string = ''
    
    for j in range(len(indices)):
        new_node = 'X' + str(i)
        rule[indices[j]] = new_node
        string += stringify([new_node] + [terminals[j]])
    
    return string, rule

# Replaces first two elements in given
# rule with a new nonterminal. Adds
# new rule to the output, returns
# altered rule
def replace_long(rule, i):
    
    new_node = 'X' + str(i)
    string = stringify([new_node] + rule[1:3])
    rule = [rule[0]] + [new_node] + rule[3:]
    
    return string, rule

# Converts long and hybrid productions to
# CNF form, adds string to output
def convert_long_and_hybrid(filename):
    
    output = ''
    reserves = []
    i = 1
    top = ''
    tops = ''
    first = True
    
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            line = line.strip()
            
            # do not process commented or empty lines
            if line != '' and line[0] != '#':
                line = line.split('->')
                lhs = line[0].strip()
                
                # store initial symbol
                if first:
                    top = lhs
                    first = False
                    
                rhs = line[1:][0].strip().split('|')
                
                for item in rhs:
                    rule = [lhs] + item.split()
                    skip = False
                    
                    # reserve unit productions for the end
                    if len(rule) == 2 and rule[1][0] != "'":
                        reserves.append(rule)
                        skip = True
                    
                    # not a terminal
                    elif len(rule) > 2:
                        
                        # find hybrid rules
                        terminals, indices = find_terminals(rule)
                        if len(terminals) > 0:
                            string, rule = replace_terminals(rule, \
                                terminals, indices, i)
                            if rule[0] == top:
                                tops += string
                            else:
                                output += string
                            i += 1
                            
                        # convert long productions
                        while len(rule) > 3:
                            string, rule = replace_long(rule, i)
                            if rule[0] == top:
                                tops += string
                            else:
                                output += string
                            i += 1
                    
                    add_rule(rule)
                    
                    if not skip:    # don't output unit productions:
                        if rule[0] == top:
                            tops += stringify(rule)
                        else:
                            output += stringify(rule)   # output final rule
                        
    return top, tops, output, reserves

# Conerts unit productions to CNF form
# and adds to output string
def convert_unit(reserves, top):
    
    global rule_map
    
    output = ''
    tops = ''
    
    # convert unit productions 
    while len(reserves) > 0:
        rule = reserves.pop()
        if rule[1] in rule_map:
            for item in rule_map[rule[1]]:
                new_rule = [rule[0]] + item
                
                # if not a unit production anymore, output
                if len(new_rule) > 2 or new_rule[1][0] == "'":
                    if new_rule[0] == top:
                        tops += stringify(new_rule)
                    else:
                        output += stringify(new_rule)
                
                # still a unit production, recycle
                else:
                    reserves.append(new_rule)
                    
                add_rule(new_rule)
        
    return tops, output

# Reads in CFG file, converts to Chomsky
# Normal Form and outputs to file
def main():
    
    if len(sys.argv) < 3:
        sys.stdout.write('Comverter takes two arguments: \
            [input_grammar_file] [out_file]\n')
        sys.exit()
    
    top, tops, output, reserves = convert_long_and_hybrid(sys.argv[1])
    results = convert_unit(reserves, top)
    tops += results[0]
    output += results[1]
    
    with open(sys.argv[2], 'w') as f:
        f.write(tops)
        f.write(output)

main()
            
