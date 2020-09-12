from Block import *

'''
Variables Blocks
'''
def setVariableTo(variableName, value) : return Block('doSetVar', [Option(variableName), value])
def changeVariableBy(variableName, value) : return Block('doChangeVar', [Option(variableName), value])
def showVariable(variableName) : return Block(Option('doShowVar'), [variableName])
def hideVariable(variableName) : return Block(Option('doHideVar'), [variableName])
def scriptVariables(variableNames : [str]) : return Block('doDeclareVariables', variableNames)
def inherit(parent) : return Block('doDeleteAttr', [Option(parent)])
def newList(values) : return Block('reportNewList', values)
def numbersFrom(start, stop) : return Block('reportNumbers', [start, stop])
def inFrontOf(value , lst) :  return Block('reportCONS', [value, lst])
def itemOf(index, lst) : return Block('reportListItem', [index, lst])
def allButFirstOf(lst) : return Block('reportCDR', [lst])
def lengthOf(lst) : return Block('reportListLength', [lst])
def indexOf(item, lst) : return Block('reportListIndex', [item, lst])
def contains(lst, item) : return Block('reportListContainsItem', [lst, item])
def isEmpty(lst) : return Block('reportListIsEmpty', [lst])
def mapOver(ring, lst) : Block('reportMap', [ring, lst])
def keep(ring, lst) : Block('reportKeep', [ring, lst])
def combine(lst, ring) : Block('reportCombine', [lst, ring])
def findFirst(ring, lst) : Block('reportFindFirst', [ring, lst])
def forEach(varName, lst, script) : Block('doForEach', [varName, lst, script])
def append(lists : []) : Block('reportConcatenatedLists', lists)
def addTo(value, lst) : Block('doAddToList', [value, lst])
def deleteIndex(index, lst) : Block('doDeleteFromList', [index, lst])
def insertAt(item, index, lst) : Block('doInsertInList', [item, index, lst])
def replaceItem(index, lst, item) : Block('doReplaceItemInList', [index, lst, item])

# # Operations that aren't real blocks
# def makeGlobalVariable(variableName) : return Block('makeGlobal', [variableName])
# def deleteGlobalVariable(variableName) : return Block('deleteGlobal', [variableName])

'''
Operator Blocks
'''

def commandRing(command) : return Block('reifyScript', [command])
def reporterRing(reporter) : return Block('reifyReporter', [reporter])
def predicateRing(predicate) : return Block('reifyPredicate', [predicate])
def plus(x, y) : return Block('reportSum', [x, y])
def subtract(x, y) : return Block('reportDiff', [x, y])
def multiply(x, y) : return Block('reportProduct', [x, y])
def divide(x, y) : return Block('reportQuotient', [x, y])
def power(x, y) : return Block('reportPower', [x, y])
def modulo(x, y) : return Block('reportModulus', [x, y])
def reportRound(x) : return Block('reportRound', [x])
def of(option, x) : return Block('reportMonadic', [Option(option), x])
def absOf(x) : return of('abs' ,x)
def negOf(x) : return of('neg', x)
def ceilOf(x) : return of('ceiling', x)
def floorOf(x) : return of('floor', x)
def sqrtOf(x) : return of('sqrt', x)
def sinOf(x) : return of('sin', x)
def cosOf(x) : return of('cos', x)
def tanOf(x) : return of('tan', x)
def asinOf(x) : return of('asin', x)
def acosOf(x) : return of('acos', x)
def atanOf(x) : return of('atan', x)
def lnOf(x) : return of('ln', x)
def logOf(x) : return of('log', x)
def binLogOf(x) : return of('lg', x)
def eTo(x) : return of('e^', x)
def tenTo(x) : return of('10^', x)
def twoTo(x) : return of('2^', x)
def identity(x) : return of('id', x)
def pickRandom(start, stop) : return Block('reportRandom', [start, stop])
def lessThan(x, y) : return Block('reportLessThan', [x, y])
def equalTo(x, y) : return Block('reportEquals', [x, y])
def greaterThan(x, y) : return Block('reportGreaterThan', [x, y])
def andOp(x, y) : return Block('reportAnd', [x, y])
def orOp(x, y) : return Block('reportOr', [x, y])
def notOp(x) : return Block('reportNot', [x])
def boolean(value) : return Block('reportBoolean', [value])
def join(words) : return Block('reportJoinWords', words)
def textSplit(text, splitString) : return Block('reportTextSplit', [text, splitString])


'''
Motion Blocks
'''

def moveSteps(steps) : return Block('forward', [steps])
def turnClockwise(degrees) : return Block('turn', [degrees])
def turnCounterClockwise(degrees) : return Block('turnLeft', [degrees])
def pointInDirection(degree) : return Block('setHeading', [degree])
def pointTowards(option) : return Block('doFaceTowards', [Option(option)])
def gotoXY(x, y) : return Block('gotoXY', [x, y])
def goto(option) : return Block('goto', [Option(option)])
def glide(seconds, x, y) : return Block('doGlide', [seconds, x, y])
def changeXBy(steps) : return Block('changeXPosition', [steps])
def setXto(location) : return Block('setXPosition', [location])
def changeYBy(steps) : return Block('changeYPosition', [steps])
def setYto(location) : return Block('setYPosition', [location])
def bounceOffEdge() : return Block('bounceOffEdge', [])
def xPosition() : return Block('xPosition', [])
def yPosition() : return Block('yPosition', [])
def direction() : return Block('direction', [])

'''
Control Blocks
'''

def greenFlag() : return Block('receiveGo', [])
def whenKeyPressed(key) : return Block('receiveKey', [Option(key)])
def whenSpriteIs(action) : return Block('receiveInteraction', [Option(action)])
def when(condition) : return Block('receiveCondition', [condition])
def whenReceived(message) : return Block('receiveMessage', [message])
def broadcast(message) : return Block('doBroadcast', [Option(message)])
def broadcastAndWait(message) : return Block('doBroadcastAndWait', [Option(message)])
def sendMessageTo(message, sprite) : return Block('doSend', [Option(message), Option(sprite)])
def message() : return Block('getLastMessage', [])
def warp(script) : return Block('doWarp', [script])
def doWait(seconds) : return Block('doWait', [seconds])
def waitUntil(condition) : return Block('doWaitUntil', [condition])
def forever(script) : return Block('doForever', [script])
def repeat(iterations, script) : return Block('doRepeat', [iterations, script])
def forLoop(variableName, start, stop, script) : return Block('doFor', [variableName, start, stop, script])
def If(condition, script) : return Block('doIf', [condition, script])
def ifElse(condition, scriptOnTrue, scriptOnFalse) : 
    return Block('doIfElse', [condition, scriptOnTrue, scriptOnFalse])
def ifThenElse(condition, valueOnTrue, valueOnFalse) : 
    return Block('reportIfElse', [condition, valueOnTrue, valueOnFalse])
def report(value) : return Block('doReport', [value])
def stop(scope) : return Block('doStopThis', [Option(scope)])
def run(command) : return Block('doRun', [command])
def launch(script) : return Block('fork', [script])
def call(script) : return Block('evaluate', [script])
def tellTo(sprite, command) : return Block('doTellTo', [sprite, command])
def askFor(sprite, reporter) : return Block('reportAskFor', [sprite, reporter])
def runWithContinuation(command) : return Block('doCallCC', [command])
def callWithContinuation(command) : return Block('reportCallCC', [command])
def whenStartAsClone(script) : return Block('receiveOnClone', [script])
def createCloneOf(sprite) : return Block('createClone', [Option(sprite)])
def newCloneOf(sprite) : return Block('newClone', [Option(sprite)])
def removeClone() : return Block('removeClone', [])


# Additional Dictionaries + functions to help with other classes and methods

OPERATOR_BLOCKS = {
    'reifyScript' : 'reporter',
    'reifyReporter' : 'reporter',
    'reifyPredicate' : 'reporter',
    'reportSum' : 'reporter',
    'reportDiff' : 'reporter',
    'reportProduct' : 'reporter',
    'reportQuotient' : 'reporter',
    'reportPower' : 'reporter',
    'reportModulus' : 'reporter',
    'reportRound' : 'reporter',
    'reportMonadic' : 'reporter',
    'reportRandom' : 'reporter',
    'reportLessThan' : 'predicate',
    'reportEquals' : 'predicate',
    'reportGreaterThan' : 'predicate',
    'reportAnd' : 'predicate',
    'reportOr' : 'predicate',
    'reportNot' : 'predicate',
    'reportBoolean' : 'predicate',
    'reportJoinWords' : 'reporter',
    'reportTextSplit' : 'reporter'
}

def isOperator(block : Block):
    return block.signature in OPERATOR_BLOCKS

def getOperatorType(block : Block):
    return OPERATOR_BLOCKS[block.signature]

    