import re, sys, pprint
import lexicalAnalysisPiece, semanticsAnalysisPiece

def reversedList(list):
    reversed = []
    for i in list:
        reversed.insert(0, i)
    return reversed
        
sortedTokens = lexicalAnalysisPiece.analyze(sys.argv)

try:
    grammarFile = open(sys.argv[5], 'r', encoding='utf-8')
except Exception as e:
    print("Error: Grammar File not found, quitting") 
    sys.exit()
    
grammarLines = grammarFile.readlines()
grammarFile.close()

rules = {}
first = {}
follow = {}

done = False
nt = True
i = 0
curNT = ''
nts = []
while(not done):
    line = grammarLines[i].strip()
    if(nt):
        curNT = line.split()[0].strip()
        nts.append(curNT)
        follow[curNT] = [i for i in line.split()[1:]]
        nt = False
    else:
        if(line[0] == '-'):
            nt = True
            i += 1
            continue
        # Add the rule for the cur NT
        if(curNT in rules.keys()):
            rules[curNT].append([i for i in line.split('|')[0].split()])
        else:
            rules[curNT] = [[i for i in line.split('|')[0].split()]]
        # Add the first of rule
        first[''.join(line.split('|')[0].split())] = [i for i in line.split('|')[1].split()]
    i += 1
    if(i == len(grammarLines)):
        done = True

stack = ['$', 'P']
i = 0
count = 1
done = False
found = False
while(not done):
    found = False
    count += 1
    # Temp error handling
    if(count == sys.maxsize):
        print('REJECT')
        break
    item = sortedTokens[i]
    # If the stack matches the item, remove it
    if(item.getSymbol() == stack[-1]):
        semanticsAnalysisPiece.terminalFound(item)
        stack.pop()
        i += 1
        # If the stack is empty and 
        if(len(stack) == 0):
            if(i == len(sortedTokens)):
                print('ACCEPT')
            else:
                print('REJECT')
            done = True
        continue
    elif(stack[-1] in nts):
        for rule in rules[stack[-1]]:
            if(item.getSymbol() in first[''.join(rule)]):
                semanticsAnalysisPiece.semanticCheck(stack[-1], rule, item)
                stack.pop()
                stack.extend(reversedList(rule))
                found = True
                break
            elif('#' == rule[0] and item.getSymbol() in follow[stack[-1]]):
                semanticsAnalysisPiece.semanticCheck(stack[-1], rule, item)
                found = True
                stack.pop()
                break
        if(not found):
            done = True
            print('REJECT')
    else:
        done = True
        print('REJECT')