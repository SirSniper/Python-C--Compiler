import re, sys

# Get source file, if unavailable, exit
try:
    grammarFile = open(sys.argv[1], 'r')
except Exception as e:
    print("Error: Grammar File not found, quitting") 
    sys.exit()
     
grammarLines = grammarFile.readlines()
grammarFile.close()
 
for line in grammarLines:
    grammarRule = re.split(r'->', line)
    nt = grammarRule[0]


def union(first, begins):
    n = len(first)
    first |= begins
    return len(first) != n

class Grammar:
    
    def __init__(self, *rules):
        self.rules = tuple(self._parse(rule) for rule in rules)
    def _parse(self, rule):
        return tuple(rule.replace(' ', '').split('::='))
        
    def __getitem__(self, nonterminal):
        yield from [rule for rule in self.rules 
                    if rule[0] == nonterminal]
        
    @staticmethod
    def is_nonterminal(symbol):
        return (symbol.isalpha() and symbol.isupper())
        
    @property
    def nonterminals(self):
        return set(nt for nt, _ in self.rules)
        
    @property
    def terminals(self):
        return set(
            symbol
            for _, expression in self.rules
            for symbol in expression
            if not self.is_nonterminal(symbol)
        )
        
        
def first_and_follow(grammar):
    # first & follow sets, epsilon-productions
    # Create a first set for each non-terminal
    first = {i: set() for i in grammar.nonterminals}
    # Add a set for each terminal to the first
    first.update((i, {i}) for i in grammar.terminals)
    #Add a set for each non-terminal to the follow set
    follow = {i: set() for i in grammar.nonterminals}
    epsilon = set()
    while True:
        updated = False
        
        for nt, expression in grammar.rules:
            # FIRST set w.r.t epsilon-productions
            # Loop through the symbols in the expression from left to right
            for symbol in expression:
                # Add the first set of the symbol to the first set of the the current non-terminal
                updated |= union(first[nt], first[symbol])
                if symbol not in epsilon:
                    # If this symbol isn't an epsilon production, break out of the for loop
                    break
                else:
                    # Otherwise, add the non-terminal set to the 
                    updated |= union(epsilon, {nt})
                
            # FOLLOW set w.r.t epsilon-productions
            
            # Get the current follow set
            aux = follow[nt]
            
            for symbol in reversed(expression):
                if symbol in follow:
                    # If the symbol is a non-terminal in the follow array, add the follow to the current 
                    print('Adding aux to follow of ' + symbol)
                    updated |= union(follow[symbol], aux)
                if symbol in epsilon:
                    print('Adding first to aux')
                    aux = aux.union(first[symbol])
                else:
                    print('Aux is now the first of ' + symbol)
                    aux = first[symbol]
        if not updated:
            return first, follow, epsilon
        
first, follow, epsilon = first_and_follow(Grammar(
    '^ ::= A $',
    'A ::= ABBC',
    'A ::= B',
    'A ::= 1',
    'B ::= C',
    'B ::= 2',
    'C ::= 3',
    'C ::= ',
))

print(follow)