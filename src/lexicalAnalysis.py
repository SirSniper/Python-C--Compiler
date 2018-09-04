import re, sys
from re import match

print(sys.argv[1])

try:
    sourceFile = open(sys.argv[1], 'r')
except Exception as e:
    print("Error: Source File not found, quitting") 
    sys.exit()
    
sourceLines = sourceFile.readlines();

# Create main token class

class Token:
    abv = 'GEN'
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return self.abv + ': ' + self.value
        
    pass

# Token Subclasses

class Relational(Token):
    abv = 'REL'
    
    pass

class Keyword(Token):
    abv = 'KEYWORD'
        
    pass

class Identifier(Token):
    abv = 'IDENTIFIER'
    
    pass

class Delimiter(Token):
    abv = 'DELIM'
    
    pass

class Error(Token):
    abv = 'ERROR'
    
    pass

# Removes None and Space values from return

def simplify(x):
    return x

# Iterable counter
def count_iterable(i):
    return sum(1 for e in i)

# Multi-line comment Handling function
commentDepth = 0

def handleComments():
    global i, commentDepth
    
    multiline = re.compile(r'\/\*|\*\/')
    
    beginMultiline = re.compile(r'\/\*')
    
    endMultiline = re.compile(r'\*\/')

    singleLine = re.compile(r'\\\\')
    
    justStart = re.compile(r'(\/\*((?!\*\/|\/\*).)*)')

    print('INPUT: ' + sourceLines[i].strip())
    
    strippedLine = sourceLines[i]
        
    
    # Create an iterator for all multiline character matches
    lineCommentChars = multiline.findall(strippedLine)
    
    # Check to see if there were any multiline chars
    if(len(lineCommentChars) > 0):
        for match in lineCommentChars:
            # check line for /* or */
            if(match == '/*'):
                # if /*, increment depth as we have found another internal Comment
                commentDepth += 1
                
                # Remove content up to next comment char
                strippedLine =  re.sub(re.escape(justStart.search(strippedLine).group(0)), '', strippedLine, count=1)
            else:
                # if */, decrement depth as we have closed a Comment
                if(commentDepth > 0):
                    commentDepth -= 1
                    if(commentDepth == 0):
                        print('Closes Comment, need to check if all before was in comment or not, how to solve?')
                        strippedLine = re.sub(endMultiline, '', strippedLine, count=1)
                    else:
                        strippedLine = re.sub(endMultiline, '', strippedLine, count=1)
                    print(strippedLine)
            print(commentDepth)    
                
                
    # If no multiline chars, check if already in a multiline
    elif(commentDepth > 0):
        # If in a multiline, nothing should be processed
        return ''
    else:
        print('Still in comment')
    
    # Check if eof, if eof we have reached the end of the source code and everything is a Comment
    
    return re.sub(r'\\\\.*', '', strippedLine).strip();


# Loop Through All lines and create an array of tokens in order

delimiters = r'(\{|\}|\(|\)|;)|(\d+)|(\d+\.\d+)|(\<|>|==)|\s'

i = 0
numLines = len(sourceLines)

delims = re.compile(delimiters)

sortedTokens = []

while i < numLines:
    curLine = handleComments()
    # Run regex to split string
    
    tokens = filter(simplify, delims.split(curLine))
    
    # Loop through all of the tokens, check to see what form they match up with and create an appropriate object
    for token in tokens:
        if(token in delimiters):
            delim = Delimiter(token)
            sortedTokens.append(delim)
            print(delim)
        else:
            print(token)
    
    i += 1

print(sortedTokens)
    




