import re, sys, pprint

# Get source file, if unavailable, exit
try:
    grammarFile = open(sys.argv[1], 'r')
except Exception as e:
    print("Error: Grammar File not found, quitting") 
    sys.exit()
    
grammarLines = grammarFile.readlines()
grammarFile.close()

rules = {}  

for line in grammarLines:
    grammarRule = re.split(r'->', line)
    #print(grammarRule)
    rules[grammarRule[0].strip()] = [[k for k in s.split()] for s in re.split(r'\|', grammarRule[1])];
        

pprint.pprint(rules) 
newRules = {}


for nt, curRule in rules.items():
    leftRecur = []
    okRules = []
    for rule in curRule:
        print(nt)
        if(rule[0] == nt):
            leftRecur.append(rule)
#             print('Left Recursion')
#             print(nt)
#             print(rule)
#             print()
        else:
            holderRule = rule.copy()
            if(not holderRule == ['^']):
                holderRule.append(nt + '\'')
            else:
                okRules.append([nt + '\''])
            okRules.append(holderRule)
        
    if(leftRecur):
        print()
        for s in leftRecur:
            s.append(nt + '\'')
            s.pop(0)
        leftRecur.append(['^'])
        newRules[nt] = okRules
        newRules[nt + '\''] = leftRecur
    else:
        newRules[nt] = rules[nt]  
        
epsilon = []
nonterminals = []
for nt, rule in newRules.items():
    nonterminals.append(nt)
    if(['^'] in rule):
        epsilon.append(nt)
        
pprint.pprint(rules) 
pprint.pprint(newRules) 


def checkIndirectRecursion(nt, rule, grammar, path):
    global epsilon
    global nonterminals
    print('New Instance: ' + nt)
    for possibility in rule:
        if(possibility[0] == nt):
            print('Indirect recursion found')
            print(path)
        else:
            if(possibility[0] in nonterminals):
                print(path + ' -> ' + ' '.join(possibility))
                checkIndirectRecursion(nt, grammar[possibility[0]], grammar, path + ' -> ' + ' '.join(possibility))
                for i, first in enumerate(possibility):
                    if(first in epsilon and i+1 < len(possibility)):
                        print(path + ' -> ' + ' '.join(possibility[i+1:]))
                        checkIndirectRecursion(nt, grammar[possibility[i+1]], grammar, path + ' -> ' + ' '.join(possibility[i+1:]))
                    else:
                        break
            else:
                print(path + ' -> ' + ' '.join(possibility))
    return False


for nt in nonterminals:
    checkIndirectRecursion(nt, newRules[nt], newRules, nt)

for key, rule in newRules.items():
    rulesString = ''
    for item in rule:
        rulesString += ' '.join(item)
        rulesString += ' | '
    print(key + ' -> ' + rulesString[:len(rulesString)-2])

print(epsilon)