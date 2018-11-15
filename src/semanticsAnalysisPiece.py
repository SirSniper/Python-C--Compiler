from lexicalAnalysisPiece import Identifier, Number
import pprint, re, sys

class Function:
        
    def __init__(self, id, parameters, returnType):
        self.id = id
        self.params = parameters
        self.returnType = returnType
        
    def isCall(self, callArgs):
        if(len(self.params) == len(callArgs)):
            for i in range(0, len(self.params)):
                if(not callArgs[i] == self.params[i].type):
                    return False
            return True
        else:
            return False
        
    def __eq__(self, other):
        return self.id == other
    
    
    pass
        
class Var:
        
    def __init__(self, id, type, isArray=False):
        self.id = id
        self.type = type
        self.isArray = isArray
        
    def __eq__(self, other):
        return self.id == other
    
    pass

def reject(message = ""):
    print("REJECT")
    sys.exit()

needToHoldFunctionData = ['D', ['T','id','H']]
needToHoldData = ['DV', ['T','id','Y']]
fInstantiation = ['H', ['(','PS',')', 'C']]
fCall = ['L', ['(', 'AR', ')']]
vInstantiation = ['Y', [';']]
vInstantiationArray = ['Y', ['[','n',']',';']]
voidParams = ['PS', ['v', 'ZZ']]
newParam = ['PS',['K','id','X', "PL'"]]
arrayParam = ['X', ['[',']']]
moreParams = ['PA',['T','id','X']]
endParams = ["PL'",['#']]
newArgs = ['AL', ['E', "AL'"]]
moreArgs = ["AL'", [',' , 'E', "AL'"]]
endArgs = ["AL'", ['#']]
noArgs = ['AR', ['#']]
expression = ['E']
returnStatement = ['RS']

function, idListen, inExpression, typeListen, isArray, returnState, storeVar, storeFunc, newParams, endFunc, mainFound, returnFound = False, False, False, False, False, False, False, False, False, False, False, False

type, id, expressionType, funcName, funcType = "", "", "", "", ""
params = []
eStack = []
functionSymbol, varSymbol = [[]], [[]]
depth = 0

def inVar(id):
    global depth, varSymbol
    for table in varSymbol[::-1]:
        for var in table:
            if(id == var):
                return var
    return False

def inFunc(id):
    global depth, functionSymbol
    for table in functionSymbol[:depth+1]:
        for func in table:
            if(id == func):
                return func
    return False

def inTables(id):
    return inVar(id) or inFunc(id)

def checkFunctionCall():
    global eStack, endFunc
    endFunc = False
    args = []
    endArgs = False
    for item in eStack[::-1]:
        match = re.match('F-(.+)', item)
        if(match):
            func = inFunc(match.group(1))
            if(func):
                eStack.pop()
                eStack.append(func.returnType)
                return func.isCall(args)
        elif(endArgs):
            return False
        elif(item == "|"):
            eStack.pop()
        elif(item == "("):
            eStack.pop()
            endArgs = True
        else:
            args.insert(0, item)
            eStack.pop()
    return False


def validateStack():
    global eStack
    change = True
    while(change):
        change = False
        if(len(eStack) > 1):
            if(eStack[-1] == eStack[-2]):
                eStack.pop()
                change = True
            elif(eStack[-1] == "]" and len(eStack) > 3):
                if(eStack[-2] == "int" and eStack[-3] == "["):
                    eStack.pop()
                    eStack.pop()
                    eStack.pop()
                    if(eStack[-1] == "intA"):
                        eStack.pop()
                        eStack.append("int")
                        change = True
                    elif(eStack[-1] == "floatA"):
                        eStack.pop()
                        eStack.append("float")
                        change = True
                    else:
                        reject()
            
                        
def terminalFound(terminal):
    global typeListen, idListen, inExpression, depth, returnState, functionSymbol, varSymbol, returnFound, isArray, mainFound, id, type, returnFound, storeVar, storeFunc 
    global endFunc, newParams, params, function, eStack, funcName, funcType, expressionType
    if(function):
        funcName = id
        if(id.lower() == "main" and type == "void"):
            mainFound = True
        funcType = type
        id, type, function = "", "", False
        
    if(terminal.value == "$" and not mainFound):
        reject("No Main")
    
    if(mainFound == "Done" and depth == 0 and not terminal.value == '$'):
        reject("Code after main")
    
    # Increment/Decrement scope if need be
    if(terminal.value == "{"):
        depth = depth + 1
        if(len(functionSymbol) <= depth):
            functionSymbol.append([])
            varSymbol.append(params.copy())
        else:
            functionSymbol[depth] = []
            varSymbol[depth] = params.copy()
        params = []
    elif(terminal.value == "}"):
        functionSymbol.pop()
        varSymbol.pop()
        if(mainFound):
            mainFound = "Done"
        depth = depth - 1
        if(depth == 0):
            if(not funcType == "void" and not returnFound):
                reject("No valid return statement")
            returnFound = False
            funcType = ""
    
    # If we are evaluating an expression, add any ids and relevant chars to stack
    if(inExpression):
        if(isinstance(terminal, Identifier)):
            if(inTables(terminal.value)):
                cur = inVar(terminal.value)
                funcName = terminal.value
                if(cur):
                    eStack.append(cur.type + ("A" if cur.isArray else ""))
                else:
                    cur = inFunc(terminal.value)
                    eStack.append("F-"+cur.id)
                    funcName = ""
            else:
                reject("Undefined Identifier")
        elif(isinstance(terminal,  Number)):
            if(terminal.isFloat()):
                eStack.append('float')
            else:
                eStack.append('int')
        elif(terminal.value == "[" or terminal.value == "]" or terminal.value == "("):
            eStack.append(terminal.value)
            validateStack()
        elif(terminal.value == ")" and not endFunc):
            validateStack()
            if(len(eStack) > 1):
                if(eStack[-2] == "("):
                    eStack.pop(-2)
        elif(endFunc):
            endFunc = False
        if(terminal.value == ";" or terminal.value == "{"):
            inExpression = False
            validateStack()
            if(len(eStack) > 1):
                reject("Invalid expression")
            else:
                if(len(eStack) == 0):
                    expressionType = "void"
                else:
                    expressionType = eStack[0]
                if(returnState):
                    returnState = False
                    if(not funcType == expressionType):
                        reject("Invalid return type")
                    else:
                        returnFound = True
                eStack = []
            
            
    if(typeListen and not terminal.value == ","):
        type = terminal.value
        typeListen = False
        idListen = True
    elif(idListen):
        id = terminal.value
        idListen = False
        if(newParams):
            params.append(Var(id, type, False))
            id, type, newParams = "","", False
        
    # If we are instantiating a variable, set details
    if(storeVar):
        if(id in varSymbol[depth] or id in functionSymbol[depth]):
            reject("Duplicately defined id")
        if(type == "void"):
            reject("No variables of type void")
        varSymbol[depth].append(Var(id,type,isArray))
        type, id, isArray, storeVar = "", "", False, False
        
    if(storeFunc):
        if(funcName in functionSymbol[depth] or id in varSymbol[depth]):
            reject("Duplicately defined id")
        functionSymbol[depth].append(Function(funcName,params,funcType))
        funcName, storeFunc = "", False
        

def semanticCheck(nt, rule, token):
    global typeListen,inExpression, functionSymbol, isArray, storeVar, storeFunc, function, newParam, newParams, returnState, endFunc, params, endParams, moreParams, funcName
    
    if(nt == expression[0]):
        inExpression = True
    if(nt == needToHoldData[0] or nt == needToHoldFunctionData[0]):
        typeListen = True
        if(nt == needToHoldFunctionData[0]):
            function = True
    if(nt == returnStatement[0]):
        returnState = True
    if(nt == fInstantiation[0] and rule == fInstantiation[1]):
        function = True
    if(nt == fCall[0] and rule == fCall[1]):
        inExpression = True
        if(not re.match('F-(.+)', eStack[-1])):
            eStack[-1] = "F-" + funcName
            funcName = ""
    if(nt == vInstantiation[0] and rule == vInstantiation[1]):
        storeVar = True
    if(nt == vInstantiationArray[0] and rule == vInstantiationArray[1]):
        storeVar = True
        isArray = True
    if((nt == noArgs[0] and rule == noArgs[1]) or (nt == endArgs[0] and rule == endArgs[1])):
        checkFunctionCall()
        endFunc = True
    if(nt == moreArgs[0] and rule == moreArgs[1]):
        validateStack()
        eStack.append("|")
    if(nt == voidParams[0] and rule == voidParams[1]):
        functionSymbol[depth].append(Function(id, [], type))
    if(nt == newParam[0] and rule == newParam[1]):
        typeListen = True
        newParams = True
    if(nt == moreParams[0] and rule == moreParams[1]):
        typeListen = True
        newParams = True
    if(nt == arrayParam[0] and rule == arrayParam[1]):
        params[-1].isArray = True
    if(nt == endParams[0] and rule == endParams[1]):
        storeFunc = True
    