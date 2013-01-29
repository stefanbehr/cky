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

def get_grammar(filename):
    
    global rule_map
    global word_map
    
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            line = line.strip()
            if line != '' and line[0] != '#':
                line = line.split('->')
                lhs = line[0].strip()
                rhs = line[1].strip()
                
                # nonterminals
                if rhs[0] != "'":
                    rhs = rhs.split()
                    if rhs[0] not in rule_map:
                        rule_map[rhs[0]] = {rhs[1]:[lhs]}
                    elif rhs[1] not in rule_map[rhs[0]]:
                        rule_map[rhs[0]][rhs[1]] = [lhs]
                    else:
                        rule_map[rhs[0]][rhs[1]].append(lhs)
                        
                # preterminals
                else:
                    rhs = rhs.strip("'")
                    if rhs not in word_map:
                        word_map[rhs] = []
                    word_map[rhs].append(lhs)
                    
def get_sentences(filename):
    sentences = []
    
    with open(filename) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            sentence = line.strip()
            if sentence != '':
                sentence = re.sub(r'([\.,%?!])', r' \1 ', sentence).strip()
                sentence = sentence.split()
                sentences.append(sentence)
        
    return sentences

def parse(sentence):
    
    global rule_map
    global word_map
    global name
    
    # assumes no decimals
    N = len(sentence)
    chart = [None] * (N + 1)
    
    for j in range(1, N + 1):
        chart[j] = [None] * j
        token = sentence[j - 1]
        preterms = give_names(word_map[token], None, token)
        chart[j][j - 1] = preterms
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                if chart[k][i] is not None\
                and chart[j][k] is not None:
                    Bs = chart[k][i]
                    Cs = chart[j][k]
                    terms = []
                    for B in Bs:
                        for C in Cs:
                            if B[0] in rule_map:
                                if C[0] in rule_map[B[0]]:
                                    nonterms = give_names(rule_map[B[0]][C[0]],\
                                        [k, i, B[3]], [j, k, C[3]])
                                    terms += nonterms
                    if len(terms) > 0:
                        if chart[j][i] is None:
                            chart[j][i] = terms
                        else:
                            chart[j][i] += terms
    
    return chart


def give_names(terms, orig_j, orig_i):
    
    global name
    
    terms2 = []
    for term in terms:
        terms2.append([term, orig_j, orig_i, name])
        name += 1
    
    return terms2
    
def find_roots(root_list):
    
    roots = []
    
    for element in root_list:
        if element[0] == 'TOP':
            roots.append(element)

    return roots
    
def backtrack(chart):
    parses = []
    
    for root in chart[len(chart) - 1][0]:
        if root[0] == 'TOP':
            parses.append(retrace(root, chart, 0).strip())
    
    return parses

def retrace(node, chart, depth):
    
    global stop_phrases
    
    if node[1] is None:
        return ' (' + node[0] + " '" + node[2] + "')"
    
    output = ' (' + node[0]
    left_index = find_node(chart, node[1][0], node[1][1], node[1][2])
    right_index = find_node(chart, node[2][0], node[2][1], node[2][2])
    output += retrace(chart[node[1][0]][node[1][1]][left_index], chart, depth + 1)
    output += retrace(chart[node[2][0]][node[2][1]][right_index], chart, depth + 1)
    output += ')'
    
    return output
    
def find_node(chart, j, i, name):
    nodes = chart[j][i]
    i = 0
    for node in nodes:
        if node[3] == name:
            return i
        i += 1

# Returns parses in string representation
def print_parses(parses):
    output = ''
    
    for parse in parses:
        parse = parse.split()
        output += print_tree(parse)
        output += '\n\n'
    
    return output

# Returns a string representation of
# a given tree
def print_tree(parse):
    
    string = parse[0]
    open_paren = 1
    depth = 1
    index = 1
    
    while open_paren > 0 and index < len(parse):
        if parse[index][0] != "'":
            string += '\n' + '  ' * depth + parse[index]
            open_paren += 1
            depth = open_paren
        else:
            string += ' ' + parse[index]
            open_paren -= close_paren(parse[index])
            depth = open_paren
            
        index += 1
                
    return string
    
# Returns number of close parentheses attached
# to a token
def close_paren(string):
    num = 0
    index = -1
    
    while string[index] == ')':
        num += 1
        index -= 1

    return num

get_grammar(sys.argv[1])
sentences = get_sentences(sys.argv[2])

sentence_num = 1
for sentence in sentences:
    chart = parse(sentence)
    if chart[len(sentence)][0] is not None:
        parses = backtrack(chart)
        output += print_parses(parses)
        output += str(sentence_num) + '\n'
        output += '-' * 40 + '\n\n'
    sentence_num += 1

print output
    












    