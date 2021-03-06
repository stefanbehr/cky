#!/usr/bin/env python2.7

"""
Kathryn Nichols
Stefan Behr
LING 571
Project 1
"""

import re

class CNFGrammar:
    """
    Class for CFGs in Chomsky Normal Form
    """
    def __init__(self, path):
        """
        Reads CFG from file at path argument, creating object
        attributes with all lexical tree productions and phrase
        tree productions in the grammar.
        """

        self.lexical = {}  # unary branching grammar productions
        self.phrasal = {}  # binary branching grammar productions
        self.start = None  # start symbol

        with open(path) as grammar_file:
            grammar_text = grammar_file.read()

        grammar_text = grammar_text.strip()
        grammar_lines = grammar_text.split("\n")

        production = r"""^(\w+)\s*->\s*(\w+\s+\w+|'\S+'|"\S+")$"""
        quoted = r"""^"\S+"|'\S+'$"""
        PRODUCTION = re.compile(production)
        QUOTED = re.compile(quoted)

        for line in grammar_lines:
            prod_match = PRODUCTION.match(line)
            if prod_match:
                lhs, rhs = prod_match.group(1), prod_match.group(2)
                if not self.start:
                    self.start = lhs
                quot_match = QUOTED.match(rhs)
                if quot_match:
                    prod_type = "lexical"
                else:
                    prod_type = "phrasal"
                    rhs = rhs.split()
                rule_map = getattr(self, prod_type)
                if lhs not in rule_map:
                    rule_map[lhs] = []
                rule_map[lhs].append(rhs)

    def lhs_for_rhs(self, rhs, structure_type):
        """
        Returns a list of nonterminal symbols which
        are found on the left sides of productions 
        whose right-hand sides are equivalent to rhs.
        Searches lexical or phrasal productions depending
        on structure_type argument.
        """
        nonterminals = []
        productions = getattr(self, structure_type)
        for lhs in productions:
            if rhs in productions[lhs]:
                nonterminals.append(lhs)
        return nonterminals

class Node:
    """
    Class for nodes in placed into CKY parse chart
    """
    def __init__(self, symbol, left=None, right=None, terminal=None):
        """
        Given a node symbol and left and right child 
        'pointers', creates a node containing this 
        information.

        My docstrings suck.
        """
        self.symbol = symbol
        self.left = left
        self.right = right
        self.terminal = terminal

    def __str__(self):
        """
        'To string' method.
        """
        return """({0} -> {1} {2})""".format(self.symbol, str(self.left), str(self.right))

class CKYParser:
    """
    CKY parsing algorithm class
    """
    def __init__(self, path):
        """
        Creates a parser which can parse input
        strings using the grammar defined in the file
        found at the path argument.
        """
        self.grammar = CNFGrammar(path)

    def parse(self, sentence):
        """
        Given an input sentence in the form of a list of tokens, 
        attempts to parse the string according to the grammar in 
        self.grammar, and returns a list of parse trees.
        """
        N = len(sentence)

        # initializes (N+1)x(N+1) matrix to None.
        # using only list multiplication yields array
        # of pointers to same array.
        self.chart = [(N+1)*[None] for row_label in xrange(N+1)]
        for j in xrange(1, N+1):
            token = sentence[j-1]
            self.chart[j-1][j] = map(lambda preterm: Node(preterm, terminal=token), self.grammar.lhs_for_rhs(token, "lexical"))
            for i in reversed(xrange(0, j-1)):  # j-2..0
                for k in xrange(i+1, j):        # i+1..j-1
                    lcandidates = self.chart[i][k]  # candidate left branches
                    rcandidates = self.chart[k][j]  # candidate right branches
                    # look at all node pairs from two split cells
                    # check if node pair is on RHS of any production
                    # and add node to appropriate cell
                    if lcandidates and rcandidates:
                        for lnode in lcandidates:
                            lsymbol = lnode.symbol
                            for rnode in rcandidates:
                                rsymbol = rnode.symbol
                                # all mother node symbols that can dominate current pair
                                # of node symbols
                                msymbols = self.grammar.lhs_for_rhs([lsymbol, rsymbol], "phrasal")
                                if msymbols and self.chart[i][j] is None:
                                    self.chart[i][j] = []
                                for msymbol in msymbols:
                                    self.chart[i][j].append(Node(msymbol, lnode, rnode))

    def parse_to_string(self, node):
        """
        Given the root node of a parse, return a string 
        representation of the parse.
        """
        if node.left and node.right:
            inside = "{0} {1}".format(self.parse_to_string(node.left), self.parse_to_string(node.right))
        else:
            inside = "{0}".format(node.terminal)
        return "({0} {1})".format(node.symbol, inside)

    def get_parses(self, sentence):
        """
        Given a sentence, generates a parse chart for it, 
        and returns a list of string representations of all 
        of its parses.
        """
        self.parse(sentence)
        N = len(sentence)
        parse_roots = self.chart[0][N]
        result = []
        if parse_roots: # guard against None
            for root in parse_roots:
                if root.symbol == self.grammar.start:
                    result.append(self.parse_to_string(root))
        return result
