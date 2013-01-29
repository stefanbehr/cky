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