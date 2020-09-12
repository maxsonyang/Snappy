from Blocks import Block

class CustomBlock(Block):
    '''
    
    '''

    def __init__(self, 
        signature, 
        inputs : [], 
        inputTypes : [], 
        inputCount, 
        blockDefinition : []
    ):
        super().__init__(signature, inputs, inputCount)