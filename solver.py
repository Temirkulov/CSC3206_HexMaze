from enum import Enum, auto
from typing import List, Tuple

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

# define the dictionary
# x and y coordinates used (x is left-right, y is up-down)
WORLD = {
    (0, 0): CellType.ENTRY,
    (0, 4): CellType.REWARD1,
    (1, 1): CellType.TRAP2,
    (1, 3): CellType.TRAP4,
    (1, 4): CellType.TREASURE,
    (1, 6): CellType.TRAP3,
    (1, 8): CellType.OBSTACLE,
    (2, 2): CellType.OBSTACLE,
    (2, 4): CellType.OBSTACLE,
    (2, 7): CellType.REWARD2,
    (2, 8): CellType.TRAP1,
    (3, 0): CellType.OBSTACLE,
    (3, 1): CellType.REWARD1,
    (3, 3): CellType.OBSTACLE,
    (3, 5): CellType.TRAP3,
    (3, 6): CellType.OBSTACLE,
    (3, 7): CellType.TREASURE,
    (3, 9): CellType.TREASURE,
    (4, 2): CellType.TRAP2,
    (4, 3): CellType.TREASURE,
    (4, 4): CellType.OBSTACLE,
    (4, 6): CellType.OBSTACLE,
    (4, 7): CellType.OBSTACLE,
    (5, 5): CellType.REWARD2
    }

# define the size of the world (6 rows, 19 columns)
WORLD_SIZE = (6, 10) 

# six axial directions (pointy-top)
DIRS: List[Tuple[int, int]] = [
    (+1, 0), (+1, -1), (0, -1),
    (-1, 0), (-1, +1), (0, +1)
]
