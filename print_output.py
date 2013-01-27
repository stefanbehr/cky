# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 18:24:20 2013

@author: kathryn
"""

stop_phrases = ['(TOP', '(S', '(SQ', '(FRAG', '(NP', '(VP', '(PP', '(ADJP', '(ADVP',\
        '(PUNC']

# Returns parses in string representation
def print_parses(sentences):
    output = ''
    sentence_num = 1
    
    for sentence in sentences:
        for parse in sentence:
            parse = parse.split()
            output += print_tree(parse)
            output += '\n\n'
        output += str(sentence_num) + '\n' + '-' * 40 + '\n'
        sentence_num += 1
    
    return output

# Returns a string representation of
# a given tree
def print_tree(parse):
    
    global stop_phrases
    
    string = parse[0]
    open_paren = 1
    depth = 1
    index = 1
    
    while open_paren > 0 and index < len(parse):
        if parse[index] in stop_phrases:
            string += '\n' + '  ' * depth + parse[index]
            open_paren += 1
            depth = open_paren
        elif parse[index][0] == '(':
            string += ' ' + parse[index]
            open_paren += 1
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


