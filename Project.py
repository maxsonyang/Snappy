from SnapBlocks import *
from Block import Script
from typing import Any
import random
import math

class Project:

    def __init__(self):
        self.globalVariables = {}
        self.executor = Executor(self)
        self.scripts = []

    def addGlobalVariable(self, variableName):
        if variableName not in self.globalVariables:
            self.globalVariables[variableName] = None
        else:
            raise ValueError(f'{variableName} already exists as a global variable!')

    def setGlobalVariable(self, variableName, value):
        if variableName not in self.globalVariables:
            raise ValueError(f'{variableName} is not a global variable')
        else:
            self.globalVariables[variableName] = value
    
    def getGlobalVariable(self, variableName : str):
        if variableName not in self.globalVariables:
            raise ValueError(f'{variableName} is not defined!')
        else:
            return self.globalVariables[variableName]

    def evaluate(self, block : Block):
        return self.executor.evaluate(block)

class Executor:
    '''
    Class that handles the execution of scripts
    in Snap. The 'how' so to speak.
    '''

    def __init__(self, project):
        self.project = project

    def execute(self, block : Block, scope : {} = None):
        self.handleVariables(block, scope)

    def evaluate(self, value : Block, scope : {} = None):
        if scope == None:
            scope = self.project.globalVariables
        if type(value) == Option:
            return value.text
        if type(value) == Variable:
            variableName = value.name
            # Check local scope first
            if variableName in scope:
                return scope[variableName]
            else:
                return self.project.getGlobalVariable(variableName)
        elif type(value) == Block:
            # and this one too.
            if isOperator(value):
                return self.handleOperator(value)
        else:
            return value

    def handleOperator(self, block : Block):
        signature = block.signature
        inputs = [self.evaluate(inp) for inp in block.inputs]

        if signature == 'reportSum':
            return inputs[0] + inputs[1]
        elif signature == 'reportDiff':
            return inputs[0] - inputs[1]
        elif signature == 'reportProduct':
            return inputs[0] * inputs[1]
        elif signature == 'reportQuotient':
            return inputs[0] / inputs[1]
        elif signature == 'reportPower':
            return inputs[0] ** inputs[1]
        elif signature == 'reportModulus':
            return inputs[0] % inputs[1]
        elif signature == 'reportRound':
            return round(inputs[0])
        elif signature == 'reportMonadic':
            return self.handleMonadic(block)
        elif signature == 'reportRandom':
            start = inputs[0]
            stop = inputs[1]
            if type(start) == int and type(stop) == int:
                return random.randint(start, stop)
            else:
                return random.uniform(start, stop)
        elif signature == 'reportLessThan':
            return inputs[0] < inputs[1]
        elif signature == 'reportEquals':
            return inputs[0] == inputs[1]
        elif signature == 'reportGreaterThan':
            return inputs[0] > inputs[1]
        elif signature == 'reportAnd':
            return inputs[0] and inputs[1]
        elif signature == 'reportOr':
            return inputs[0] or inputs[1]
        elif signature == 'reportNot':
            return not inputs[0]
        elif signature == 'reportBoolean':
            return bool(inputs[0])
        elif signature == 'reportJoinWords':
            return ''.join(inputs)
        elif signature == 'reportTextSplit':
            return inputs[0].split(inputs[1])
        else:
            raise ValueError(f'{signature} is not an operator!')

    def handleMonadic(self, block : Block):
        operatorType = block.inputs[0].text
        operand = block.inputs[1]
        if operatorType == 'abs':
            return abs(operand)
        elif operatorType == 'neg':
            return -1 * operand
        elif operatorType == 'ceiling':
            return math.ceil(operand)
        elif operatorType == 'floor':
            return math.floor(operand)
        elif operatorType == 'sqrt':
            return math.sqrt(operand)
        elif operatorType == 'sin':
            return math.sin(operand)
        elif operatorType == 'cos':
            return math.cos(operand)
        elif operatorType == 'tan':
            return math.tan(operand)
        elif operatorType == 'asin':
            return math.asin(operand)
        elif operatorType == 'acos':
            return math.acos(operand)
        elif operatorType == 'atan':
            return math.atan(operand)
        elif operatorType == 'ln':
            return math.log(operand)
        elif operatorType == 'log':
            return math.log10(operand)
        elif operatorType == 'lg':
            return math.log(operand, 2)
        elif operatorType == 'e^':
            return math.e ** operand
        elif operatorType == '10^':
            return 10 ** operand
        elif operatorType == '2^':
            return 2 ** operand
        elif operatorType == 'id':
            return operand
        else:
            raise ValueError(f'Error! {operatorType} is not a monadic function.')

    def handleVariables(self, block : Block, scope : {}):
        if block.signature == 'doSetVar':
            # get the var name and value; evaluate both
            variableName = self.evaluate(block.inputs[0])
            value = self.evaluate(block.inputs[1], scope)
            if self.varExistsLocally(variableName, scope):
                scope[variableName] = value
            else:
                self.project.setGlobalVariable(variableName, value)

        if block.signature == 'doDeclareVariables':
            variableNames = [self.evaluate(name) for name in block.inputs]
            for name in variableNames:
                scope[name] = None

        if block.signature == 'doChangeVar':
            variableName = self.evaluate(block.inputs[0])
            increment = self.evaluate(block.inputs[1])
            if type(increment) in [float, int]:
                if self.varExistsLocally(variableName, scope):
                    # Snap has a quirk where if the variable isn't a number, change var does nothing
                    if type(scope[variableName]) in [float, int]:
                        try:
                            scope[variableName] += increment
                        except TypeError:
                            scope[variableName] = 'NaN'
                else:
                    scope = self.project.globalVariables
                    if type(scope[variableName]) in [float, int]:
                        try:
                            scope[variableName] += increment
                        except TypeError:
                            scope[variableName] = 'NaN'

        
    def varExistsLocally(self, name : str, scope : {}):
        return scope != None and name in scope


            