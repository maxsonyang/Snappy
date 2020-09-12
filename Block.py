import xml.etree.ElementTree as ET
from typing import Any

class Block:

    '''
    The base class for all Snappy blocks.
        Signature: is the name of the block that corresponds
        with its signature in XML format.

        Inputs: The values you would find given as input. Empty inputs
        must be given as some kind of NoneType value

        Input Count: The amount of input slots that exist for the block.
        Used for throwing errors in the event of having too many inputs
        which could be a problem in Python but is not present in Snap! .
    
    '''

    def __init__(self, signature : str, inputs : []):

        self.signature = signature
        self.inputs = inputs

    def toXML(self):
        return blockToXML(self)

class Variable(Block):
    '''
    Snappy Equivalent of a Variable Block
        Variables are technically blocks, but they're really just
        placeholders. They differ as an XML Element because they
        contain a var attribute and no 's' or signature attribute.
    '''

    def __init__(self, name : str):
        self.name = name

class Option:
    '''
    Just a simple wrapper class to indicate that
    a particular input for blocks is an option.
    An option refers to some kind of drop-down
    selection that appears within the Snap Interface
    like "set <variablename> to ___" for example.
    '''

    def __init__(self, text):
        self.text = text
        self.tag = None

'''
Block -> XML Methods.
Useful for converting Snappy's "block" object and any Python-defined blocks
into Snap blocks.
'''

def blockToXML(block : Block) -> str:
    '''
    Converts a Block Object into an XML String.
    '''
    # Create a new block xml element
    blockXML = ET.Element('block')

    # Set the signature
    if type(block) == Variable:
        blockXML.attrib['var'] = block.name
    else:
        blockXML.attrib['s'] = block.signature

        # Add the arguments
        for i in range(len(block.inputs)):
            blockInput = block.inputs[i]
            blockXML.append(formatBlockInput(blockInput))

    return ET.tostring(blockXML).decode('utf-8')

def formatBlockInput(inp : Any) -> ET.Element:
    '''
    Converts inputs into XML-ready formats.
    All types are implicitly converted into strings since
    every non-list datatype is effectively a string.
    '''
    if inp == None:
        return ''

    if type(inp) == Option:
        valueElement = ET.Element('l')
        optionXML = ET.Element('option')
        optionXML.text = inp.text
        valueElement.append(optionXML)
        return valueElement
       
    elif type(inp) == list:
        listElement = ET.Element('list')
        for elem in inp:
            listElement.append(formatBlockInput(elem))
        
        listReporterElement = ET.Element('block')
        listReporterElement.attrib['s'] = 'reportNewList'
        listReporterElement.append(listElement)
        return listReporterElement

    else:
        valueElement = ET.Element('l')
        valueElement.text = str(inp)
        return valueElement


'''
XML -> Block Methods
'''

def xmlToBlock(xmlString : str) -> Block:
    '''
    Converts an XMLString into a Block object.
    '''
    xml = ET.fromstring(xmlString)
    if 'var' in xml.attrib:
        return Variable(xml.attrib['var'])
    else:   
        signature = xml.attrib['s']
        inputs = formatXMLInputs(xml)
        return Block(signature, inputs)

def formatXMLInputs(blockInput : ET.Element):
    '''
    Given a particular blockInput, if it's not a list it'll try
    to convert the input to a float value or int value, then string.
    Otherwise, it returns a list value and recursively formats its elements.
    '''
    value = None
    if blockInput.text == None:
        return None

    elif type(blockInput) == Option or blockInput.tag == 'l':
        if '.' in blockInput.text:
            try:
                value = float(blockInput.text)
            except ValueError:
                value = blockInput.text
        else:
            try:
                value = int(blockInput.text)
            except ValueError:
                value = blockInput.text

    elif blockInput.attrib and blockInput.attrib['s'] == 'reportNewList':
        return formatXMLInputs(blockInput[0])

    else:
        value = []
        for elem in blockInput:
            value.append(formatXMLInputs(elem))
    
    return value

class Script:
    '''
    An ordered collection of Blocks with a scope.
    '''

    def __init__(self, blocks : [Block], scope : {str : Any}):
        self.blocks = blocks
        self.scope = scope

    def __iter__(self):
        return ScriptIterator(self.blocks)

class ScriptIterator:
    '''
    Iterator class for executing a script.
    '''

    def __init__(self, blocks):
        self.blocks = blocks
        self._index = 0

    def __next__(self):
        if self._index < len(self.blocks):
            result = self.blocks[self._index]
            self._index += 1
            return result
        raise StopIteration