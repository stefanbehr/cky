# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 20:15:27 2013

@author: kathryn
"""

import sys
import re

rule_map = {}
word_map = {}
output = ''
name = 0

# Reads in given grammar file, stores
# rules and words
def get_grammar(filename):
    
    global rule_map
    global word_map
    
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            line = line.strip()
            
            # do not process empty and commented lines
            if line != '' and not re.match(r'#', line):
                line = line.split('->')
                lhs = line[0].strip()
                rhs = line[1].strip()
                
                # store nonterminal rules
                if not re.match(r"'", rhs):
                    rhs = rhs.split()
                    if rhs[0] not in rule_map:
                        rule_map[rhs[0]] = {rhs[1]:[lhs]}
                    elif rhs[1] not in rule_map[rhs[0]]:
                        rule_map[rhs[0]][rhs[1]] = [lhs]
                    elif lhs not in rule_map[rhs[0]][rhs[1]]:
                        rule_map[rhs[0]][rhs[1]].append(lhs)
                        
                # store preterminal rules
                else:
                    rhs = rhs.strip("'")
                    if rhs not in word_map:
                        word_map[rhs] = []
                    word_map[rhs].append(lhs)
                    
# Reads in given file, returns a list
# of tokenized sentences
def get_sentences(filename):
    sentences = []
    
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            sentence = line.strip()
            
            # assumes no decimals in input
            if sentence != '':
                sentence = re.sub(r'([\.,%?!])', r' \1 ', sentence).strip()
                sentence = sentence.split()
                sentences.append(sentence)
        
    return sentences

# Parses the passed sentence and returns chart
def parse(sentence):
    
    global rule_map
    global word_map
    global name
    
    N = len(sentence)
    chart = [None] * (N + 1)
    
    # traverse columns of chart
    for j in range(1, N + 1):
        chart[j] = [None] * j
        token = sentence[j - 1]
        chart[j][j - 1] = give_names(word_map[token], None, token)
        
        # find possible constituents and store
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                if chart[k][i] is not None\
                and chart[j][k] is not None:
                    Bs = chart[k][i]
                    Cs = chart[j][k]
                    terms = []
                    
                    # match left and right nodes to constituent
                    for B in Bs:
                        for C in Cs:
                            if B[0] in rule_map and C[0] in rule_map[B[0]]:
                                terms += give_names(rule_map[B[0]][C[0]],\
                                    [k, i, B[3]], [j, k, C[3]])
                    
                    # store found constituents
                    if len(terms) > 0:
                        if chart[j][i] is None:
                            chart[j][i] = terms
                        else:
                            chart[j][i] += terms
    
    return chart

# Returns given terms as a list where
# each item is a list of the term, the
# indexes of its left daughter, the 
# indexes of its right daughter and
# a unique name
def give_names(terms, orig_j, orig_i):
    
    global name
    
    named_terms = []
    for term in terms:
        named_terms.append([term, orig_j, orig_i, name])
        name += 1
    
    return named_terms
    
# Backtracks from root node, returns a list
# of parses as bracketed labeled strings
def backtrack(chart):
    parses = []
    
    for root in chart[len(chart) - 1][0]:
        if root[0] == 'TOP':
            parses.append(retrace(root, chart, 0).strip())
    
    return parses

# Recurses on given node to generate and
# return bracketed labeled string representation 
# of parse
def retrace(node, chart, depth):
    
    # leaf node
    if node[1] is None:
        return ' (' + node[0] + " '" + node[2] + "')"
    
    # index of left and right nodes within chart cell
    left_index = find_node(chart, node[1][0], node[1][1], node[1][2])
    right_index = find_node(chart, node[2][0], node[2][1], node[2][2])

    output = ' (' + node[0]
    
    # recurse on left node
    output += retrace(chart[node[1][0]][node[1][1]][left_index], \
        chart, depth + 1)
    
    # recurse on right node
    output += retrace(chart[node[2][0]][node[2][1]][right_index], \
        chart, depth + 1)
        
    output += ')'
    
    return output

# Returns the index of the node bearing
# name at cell [j, i] in the chart
def find_node(chart, j, i, name):
    nodes = chart[j][i]
    i = 0
    for node in nodes:
        if node[3] == name:
            return i
        i += 1

# Returns parses as a string
def print_parses(parses):
    output = ''
    
    for parse in parses:
        parse = parse.split()
        output += print_tree(parse)
        output += '\n\n'
    
    return output

# Returns indented tree representation
# of given parse
def print_tree(parse):
    
    string = parse[0]
    open_paren = 1
    depth = 1
    index = 1
    
    while open_paren > 0 and index < len(parse):
        if not re.match(r"'", parse[index]):
            string += '\n' + '  ' * depth + parse[index]
            open_paren += 1
            depth = open_paren
        else:
            string += ' ' + parse[index]
            open_paren -= close_paren(parse[index])
            depth = open_paren
            
        index += 1
                
    return string
    
# Returns number of close parentheses 
# attached to a token
def close_paren(string):
    num = 0
    index = -1
    
    while string[index] == ')':
        num += 1
        index -= 1

    return num

if __name__ == '__main__':
    
    get_grammar(sys.argv[1])
    sentences = get_sentences(sys.argv[2])
    
    total = 0
    sentence_num = 1
    for sentence in sentences:
        name = 0
        chart = parse(sentence)
                    
        if chart[len(sentence)][0] is not None:
            parses = backtrack(chart)
            total += len(parses)
            output += print_parses(parses)
            output += str(sentence_num) + '\n'
            output += '-' * 40 + '\n\n'
        sentence_num += 1
    
    print output
    