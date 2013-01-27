# -*- coding: utf-8 -*-

import sys

stop_phrases = ['(TOP', '(S', '(SQ', '(FRAG', '(NP', '(VP', '(PP', \
    '(ADJP', '(ADVP', '(PUNC']

def print_tree(sentences):
    output = ''
    sentence_num = 1
    
    for sentence in sentences:
        for parse in sentence:
            parse = parse.split()
            output += print_subtree(parse)
            output += '\n\n'
        output += str(sentence_num) + '\n' + '-' * 40 + '\n'
        sentence_num += 1
    
    return output

def print_subtree(parse):
    
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
            if open_paren < depth:
                string += '\n'
            
        index += 1
                
    return string
    
    
def close_paren(string):
    num = 0
    index = -1
    
    while string[index] == ')':
        num += 1
        index -= 1

    return num

sys.stdout.write(print_tree(sentences) + '\n')

