import re, sys
from re import match

# Get source file, if unavailable, exit
try:
    sourceFile = open(sys.argv[1], 'r')
except Exception as e:
    print("Error: Source File not found, quitting") 
    sys.exit()
    
sourceLines = sourceFile.readlines()
sourceFile.close()

# Gets some language details from config files, changes to these files will still need to be updated in the regex
def getLanguageSemantics(filename, semanticsName):
    try:
        semanticsFile = open(filename, 'r')
    except Exception as e:
        print("Error: " + semanticsName + " File not found, quitting") 
        sys.exit()
        
    items = []
    lines = semanticsFile.readlines()
    for item in lines:
        items.append(item.strip())
    
    semanticsFile.close()
    return items

keywords = getLanguageSemantics(sys.argv[2], 'Keywords')
delimiters = getLanguageSemantics(sys.argv[3], 'Delimiters')
relationOperators = getLanguageSemantics(sys.argv[4], 'Relational Operators')

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
    abv = 'REL/OPERATION'
    
    pass

class Keyword(Token):
    abv = 'KEYWORD'
        
    pass

class Identifier(Token):
    abv = 'IDENTIFIER'
    
    pass

class Number(Token):
    abv = 'NUM'
    
    pass

class Delimiter(Token):
    abv = 'DELIM'
    
    pass

class Error(Token):
    abv = 'ERROR'
    
    pass

# Removes None and Space values from return, used with filter functions

def simplify(x):
    return x

# Multi-line comment Handling function-
commentDepth = 0

def handleComments():
    global i, commentDepth
    
    multiline = re.compile(r'(\/\*)|(\*\/)')
    
    if(sourceLines[i].strip()):
        print()
        print('INPUT: ' + sourceLines[i].strip())
    
    strippedLine = sourceLines[i]
    # Split the line at comment chars to be processed
    splitLine = list(filter(simplify, multiline.split(strippedLine.strip())))
    
    returnLine = ''
        
    # If we have any comment chars, process them
    if(len(splitLine) > 1):
        for match in splitLine:
            if(match == '/*'):
                # if /*, increment depth as we have found another internal Comment
                commentDepth += 1
            elif(match == '*/'):
                # If we are in a comment, we need to decrement depth
                if(commentDepth > 0):
                    commentDepth -= 1
                # If we aren't in a comment, then this is part of the string
                else:
                    returnLine += ' ' + match
            else:
                # If we aren't in a comment, add the text to the returned string, if not ignore it
                if(commentDepth == 0):
                    returnLine += ' ' + match
    # If we don't have comment chars, check if we are in a comment    
    else:
        # If we aren't in a comment, return the string after removing single line comments
        if(commentDepth == 0):
            return re.sub(r'\/\/.*', '', strippedLine).strip()
        # If the whole line is in a comment, return nothing to be processed
        else:
            return ''
    
    return re.sub(r'\/\/.*', ' ', returnLine).strip()


# This regex will be used to delimit the original string and separate it into tokens
delimitersRegex = r'(\d+(?:\.\d+)?(?:E(?:-|\+)?\d+)?)|(\{|\}|\(|\)|;|,|\[|\])|(<=|>=|<|>|==|\+|\*|-|\/|=|\!=)|\s'
delims = re.compile(delimitersRegex)

# These regexs will be used to verify token type later on
# E alone not allowed as it's a special char
identifierRegexContent = r'((?!(^E$))[a-zA-Z])+'
identifierRegex = re.compile(identifierRegexContent)

numberRegexContent = r'\d+(\.\d+)?(E(-|\+)?\d+)?'
numberRegex = re.compile(numberRegexContent)

i = 0
numLines = len(sourceLines)

sortedTokens = []

# Loop Through All lines and create an array of tokens in order


while i < numLines:
    curLine = handleComments()
    # Run regex to split string
    
    tokens = filter(simplify, delims.split(curLine))
    
    # Loop through all of the tokens, check to see what form they match up with and create an appropriate object
    for token in tokens:
        # If it's a keyword, add a keyword token
        if(token.lower() in keywords):
            keyword = Keyword(token)
            sortedTokens.append(keyword)
            print(keyword)
        # If it's a delimiter, add a delimiter token
        elif(token in delimiters):
            delim = Delimiter(token)
            sortedTokens.append(delim)
            print(delim)
        # If it's a relational/operator, add a relational token
        elif(token in relationOperators):
            relation = Relational(token)
            sortedTokens.append(relation)
            print(relation)
        # If it's an identifier, add an identifier token
        elif(identifierRegex.fullmatch(token)):
            iden = Identifier(token)
            sortedTokens.append(iden)
            print(iden)
        # If it's a number, add a number token
        elif(numberRegex.fullmatch(token)):
            num = Number(token)
            sortedTokens.append(num)
            print(num)
        # If it's none of the above, then it is an error
        else:
            error = Error(token)
            sortedTokens.append(error)
            print(error)
    i += 1

#print(str(len(sortedTokens)) + ' Individual Tokens Found')