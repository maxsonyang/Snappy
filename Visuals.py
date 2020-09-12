import xml.etree.ElementTree as ET

class Stage:

    def __init__(
        self, costumes,
        sounds, variables,
        blocks, scripts,
        sprites
    ):
        self.costumes = costumes
        self.sounds = sounds
        self.variables = variables
        self.blocks = blocks
        self.scripts = scripts
        self.sprites = sprites

class Sprite:

    def __init__(
        self, name : str,
        index : str, xCoord : int,
        yCoord : int, heading : int, 
        scale : float, volume : int,
        pan : int, rotation : int,
        draggable : bool, hidden : bool,
        costumes : str, color : (float, float, float),
        pen : str, id : int
    ):
        self.name = name
        self.index = index
        self.coords = xCoord, yCoord
        self.heading = heading
        self.scale = scale
        self.volume = volume
        self.pan = pan
        self.rotation = rotation
        self.draggable = draggable
        self.hidden = hidden
        self.costumes = costumes
        self.color = color
        self.pen = pen
        self.id = id
