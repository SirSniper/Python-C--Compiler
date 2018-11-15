import re, sys
from re import match

# Create main token class

class Token:
    abv = 'GEN'
        
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return self.abv + ': ' + self.value
    
    def getSymbol(self):
        return self.value
        
    pass

# Token Subclasses

class Relational(Token):
    abv = 'REL/OPERATION'
    
    shortenedMap ={
    '*' : 'm',
    '/' : 'm',
    '+' : 'a',
    '-' : 'a',
    '=' : '='}
    
    def getSymbol(self):
        if(self.value in self.shortenedMap.keys()):
            return self.shortenedMap.get(self.value)
        else:
            return 'r'
    
    pass

class Keyword(Token):
    abv = 'KEYWORD'
    
    shortenedMap ={
    'int' : 'i',
    'void' : 'v',
    'float' : 'f'}
    
    def getSymbol(self):
        if(self.value in self.shortenedMap.keys()):
            return self.shortenedMap.get(self.value)
        else:
            return self.value
        
    pass

class Identifier(Token):
    abv = 'IDENTIFIER'
    
    def getSymbol(self):
        return 'id'
    
    pass

class Number(Token):
    abv = 'NUM'
    floatRegex = r'(\d+(?:\.\d+)(?:E(?:-|\+)?\d+)?)|(\d+(?:E(?:-|\+)?\d+))'
    
    def getSymbol(self):
        return 'n'
    
    def isFloat(self):
        if(re.match(self.floatRegex, self.value)):
            return True
        else:
            return False
    pass

class Delimiter(Token):
    abv = 'DELIM'
    
    def getSymbol(self):
        return self.value
    
    pass

class Error(Token):
    abv = 'ERROR'
    
    def getSymbol(self):
        return ''
    
    pass


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

# Removes None and Space values from return, used with filter functions

def simplify(x):
    return x

# Multi-line comment Handling function-
commentDepth = 0

def handleComments():
    global i, commentDepth, sourceLines
    
    multiline = re.compile(r'(\/\*)|(\*\/)')
    
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


sourceLines = []
i = 0

def analyze(files):
    global i, sourceLines
    
    # Get source file, if unavailable, exit
    try:
        sourceFile = open(files[1], 'r')
    except Exception as e:
        print("Error: Source File not found, quitting") 
        sys.exit()
        
    sourceLines = sourceFile.readlines()
    sourceFile.close()

    keywords = getLanguageSemantics(files[2], 'Keywords')
    delimiters = getLanguageSemantics(files[3], 'Delimiters')
    relationOperators = getLanguageSemantics(files[4], 'Relational Operators')
    
    
    # This regex will be used to delimit the original string and separate it into tokens
    delimitersRegex = r'(\d+(?:\.\d+)?(?:E(?:-|\+)?\d+)?)|(\{|\}|\(|\)|;|,|\[|\])|(<=|>=|<|>|==|\+|\*|-|\/|=|\!=)|\s'
    delims = re.compile(delimitersRegex)
    
    # These regexs will be used to verify token type later on
    # E alone not allowed as it's a special char
    identifierRegexContent = r'((?!(^E$))[a-zA-Z])+$'
    identifierRegex = re.compile(identifierRegexContent)
    
    numberRegexContent = r'\d+(\.\d+)?(E(-|\+)?\d+)?$'
    numberRegex = re.compile(numberRegexContent)
    
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
            # If it's a delimiter, add a delimiter token
            elif(token in delimiters):
                delim = Delimiter(token)
                sortedTokens.append(delim)
            # If it's a relational/operator, add a relational token
            elif(token in relationOperators):
                relation = Relational(token)
                sortedTokens.append(relation)
            # If it's an identifier, add an identifier token
            elif(identifierRegex.match(token)):
                iden = Identifier(token)
                sortedTokens.append(iden)
            # If it's a number, add a number token
            elif(numberRegex.match(token)):
                num = Number(token)
                sortedTokens.append(num)
            # If it's none of the above, then it is an error
            else:
                error = Error(token)
                sortedTokens.append(error)
                print('Reject - Lexical error')
                sys.exit()
        i += 1
        
    end = Token('$')
    sortedTokens.append(end)
    
    return sortedTokens