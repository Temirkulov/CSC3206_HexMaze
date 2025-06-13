from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from heapq import heappop, heappush
from itertools import count
from typing import Dict, List, Tuple

# ────────────────────────── 1. Tile types ──────────────────────────
class CellType(Enum):
    EMPTY = auto()
    OBSTACLE = auto()
    TREASURE = auto()
    TRAP1 = auto()     # ← ignored
    TRAP2 = auto()
    TRAP3 = auto()
    TRAP4 = auto()
    REWARD1 = auto()
    REWARD2 = auto()
    ENTRY = auto()

# Even-q axial neighbours (pointy-top)
EVEN_COL = [(-1, 0), (+1, 0), (0, +1), (0, -1), (+1, +1), (+1, -1)]
ODD_COL  = [(-1, 0), (+1, 0), (0, +1), (0, -1), (-1, +1), (-1, -1)]

# ────────────────────────── 2. World map (your latest dict) ─────────

WORLD: Dict[Tuple[int,int],CellType] = {
    # row r = 0
    (0,0):CellType.ENTRY,  (0,1):CellType.EMPTY,(0,2):CellType.EMPTY,
    (0,3):CellType.EMPTY,  (0,4):CellType.REWARD1,(0,5):CellType.EMPTY,
    (0,6):CellType.EMPTY,  (0,7):CellType.EMPTY,(0,8):CellType.EMPTY,(0,9):CellType.EMPTY,
    # row r = 1
    (1,0):CellType.EMPTY,(1,1):CellType.TRAP2,(1,2):CellType.EMPTY,
    (1,3):CellType.TRAP4,(1,4):CellType.TREASURE,(1,5):CellType.EMPTY,
    (1,6):CellType.TRAP3,(1,7):CellType.EMPTY,(1,8):CellType.OBSTACLE,(1,9):CellType.EMPTY,
    # row r = 2
    (2,0):CellType.EMPTY,(2,1):CellType.EMPTY,(2,2):CellType.OBSTACLE,
    (2,3):CellType.EMPTY,(2,4):CellType.OBSTACLE,(2,5):CellType.EMPTY,
    (2,6):CellType.EMPTY,(2,7):CellType.REWARD2,(2,8):CellType.TRAP1,(2,9):CellType.EMPTY,
    # row r = 3
    (3,0):CellType.OBSTACLE,(3,1):CellType.REWARD1,(3,2):CellType.EMPTY,
    (3,3):CellType.OBSTACLE,(3,4):CellType.EMPTY,(3,5):CellType.TRAP3,
    (3,6):CellType.OBSTACLE,(3,7):CellType.TREASURE,(3,8):CellType.EMPTY,(3,9):CellType.TREASURE,
    # row r = 4
    (4,0):CellType.EMPTY,(4,1):CellType.EMPTY,(4,2):CellType.TRAP2,
    (4,3):CellType.TREASURE,(4,4):CellType.OBSTACLE,(4,5):CellType.EMPTY,
    (4,6):CellType.OBSTACLE,(4,7):CellType.OBSTACLE,(4,8):CellType.EMPTY,(4,9):CellType.EMPTY,
    # row r = 5
    (5,0):CellType.EMPTY,(5,1):CellType.EMPTY,(5,2):CellType.EMPTY,
    (5,3):CellType.EMPTY,(5,4):CellType.EMPTY,(5,5):CellType.REWARD2,
    (5,6):CellType.EMPTY,(5,7):CellType.EMPTY,(5,8):CellType.EMPTY,(5,9):CellType.EMPTY
}

TREASURES = [p for p,t in WORLD.items() if t is CellType.TREASURE]
T_IDX     = {p:i for i,p in enumerate(TREASURES)}
ALL_MASK  = (1<<len(TREASURES))-1
ENTRY     = next(p for p,t in WORLD.items() if t is CellType.ENTRY)

def tile(p): return WORLD.get(p, CellType.OBSTACLE)
def walkable(p): return tile(p) not in {
    CellType.OBSTACLE, CellType.TRAP1, CellType.TRAP2,
    CellType.TRAP3, CellType.TRAP4}

# ───────────── 3. State ───────────────────
@dataclass(frozen=True)
class State:
    pos:  Tuple[int,int]
    sm:   float          # step multiplier (1 or 0.5)
    em:   float          # energy multiplier (1 or 0.5)
    mask: int
    def __lt__(s,o): return (s.mask,s.pos,s.sm,s.em)<(o.mask,o.pos,o.sm,o.em)

def apply(p, sm, em, mask):
    t = tile(p)
    if t is CellType.REWARD1: em = 0.5
    if t is CellType.REWARD2: sm = 0.5
    if t is CellType.TREASURE:
        mask &= ~(1<<T_IDX[p])
    return State(p, sm, em, mask)

def neighbours(p):
    for dr,dc in (EVEN_COL if p[1]%2==0 else ODD_COL):
        r,c = p[0]+dr, p[1]+dc
        if walkable((r,c)):
            yield (r,c)

def axial(a,b):
    dq=a[1]-b[1]; dr=a[0]-b[0]
    return max(abs(dq),abs(dr),abs(dq+dr))

def h(st):
    if st.mask==0: return 0.0
    remaining=[TREASURES[i] for i in range(len(TREASURES)) if st.mask&(1<<i)]
    d = min(axial(st.pos,t) for t in remaining)
    # optimistic: future moves all at cheapest possible cost (0.5+0.5)
    return d * (st.sm * st.em)

# ───────────── 4. A* search ───────────────
def solve():
    start = apply(ENTRY, 1.0, 1.0, ALL_MASK)
    pq, seen, ctr = [], set(), count()
    heappush(pq,(h(start),0.0,next(ctr),start,[start.pos],[0.0]))
    while pq:
        f,g,_,st,path,costs = heappop(pq)
        key=(st.pos,st.mask,st.sm,st.em)
        if key in seen: continue
        seen.add(key)
        if st.mask==0: return g,path,costs
        for nb in neighbours(st.pos):
            move_cost = st.sm * st.em
            nxt = apply(nb, st.sm, st.em, st.mask)
            heappush(pq,(g+move_cost+h(nxt),g+move_cost,next(ctr),
                         nxt,path+[nb],costs+[move_cost]))
    raise RuntimeError("No path")

# ───────────── 5. Main ─────────────────────
if __name__=="__main__":
    total,path,step_costs = solve()
    print(f"Total cost : {total}")
    print(f"Moves      : {len(path)-1}")
    print("Step log (pos, cost, running):")
    running = 0.0
    for pos,c in zip(path[1:],step_costs[1:]):
        running += c
        print(f"{pos}  +{c:.1f}  (→ {running:.1f})")
    print("Path:")
    print(" → ".join(f"({r},{c})" for r,c in path))
