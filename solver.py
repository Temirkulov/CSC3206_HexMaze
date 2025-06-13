from enum import Enum, auto

# define the different cell types in the hexagonal grid
class CellType(Enum):
    EMPTY     = auto()
    OBSTACLE  = auto()
    TREASURE  = auto()
    TRAP1     = auto()
    TRAP2     = auto()
    TRAP3     = auto()
    TRAP4     = auto()
    REWARD1   = auto()
    REWARD2   = auto()
    ENTRY     = auto()
    EXIT      = auto()

# define the dictionary
WORLD = {
    (0, 0): CellType.ENTRY,
}


