# Create main token class

class Token:
    pass

# Token Subclasses

class Relational(Token):
    pass



# Multi-line comment Handling function

def handleComments():
    nextLine = 0;

    # Check if line has /*
    
    # If so, increment depth by 1
    
    # while loop for depth > 0
    
    # check line for /* or */
    
    # if /*, increment depth as we have found another internal Comment
    
    # if */, decrement depth as we have closed a Comment
    
    # Print whatever part of this line that is a comment, if all print the whole line
    
    # Check if eof, if eof we have reached the end of the source code and everything is a Comment
    
    # Return the line number on which to continue
    return nextLine;


# Loop Through All lines and create an array of tokens in order

# Run regex to split string


