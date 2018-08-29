import re, sys

print(sys.argv[1])

try:
    sourceFile = open(sys.argv[1], 'r')
except Exception as e:
    print("Error: Source File not found, quitting") 
    sys.exit()
    
sourceLines = sourceFile.readlines();

# Create main token class

class Token:
    pass

# Token Subclasses

class Relational(Token):
    pass

# Simplifies regex return

def simplify(x):
    return x


# Multi-line comment Handling function
commentDepth = 0

def handleComments():
    global i, commentDepth
    
    multiline = re.compile(r'(\/\*)(\*\\)')
    
    beginMultiline = re.compile(r'\/\*')
    
    endMultiline = re.compile(r'\*\\')

    singleLine = re.compile(r'\\\\')

    print('INPUT: ' + sourceLines[i])
    
    strippedLine = sourceLines[i]
    
    
    
    
    # If so, increment depth by 1
    
    # while loop for depth > 0
    
    # check line for /* or */
    
    # if /*, increment depth as we have found another internal Comment
    
    # if */, decrement depth as we have closed a Comment
    
    # Print whatever part of this line that is a comment, if all print the whole line
    
    # Check if eof, if eof we have reached the end of the source code and everything is a Comment
    
    return re.sub(r'\\\\.*', '', strippedLine);


# Loop Through All lines and create an array of tokens in order

delimiters = r'(\{|\}|\(|\)|;)|(\d+)|(\d+\.\d+)|(\<|>|==)|\s'

i = 0
numLines = len(sourceLines)

delims = re.compile(delimiters)

while i < numLines:
    curLine = handleComments()
    tokens = filter(simplify, delims.split(curLine))
    
    for token in tokens:
        print(token)
    
    i += 1
    

# Run regex to split string


