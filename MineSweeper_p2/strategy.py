import Minefield as mf
import random

def basic_strat(dim: int):
    minefield = mf.Minefield(dim)
    covered = []
    for c in minefield.cell_grid:
        for d in c:
            covered.append(d)
    relevant = []
    stop = 0
    score = 0
    while covered:
    #choose a random cell to uncover
        i = random.randint(0,len(covered)-1)
        cell = covered.pop(i)
        if minefield.field[cell.loc[0]][cell.loc[1]] == 1:
            stop = -1
        else:
            cell._status = cs.Cell_Status.SAFE
            relevant.append(cell)
            score += 1+stop
        while relevant:
            cell = relevant.pop(0)
            if cell._status == cs.Cell_Status.SAFE:
                if cell._clue - cell._num_mine == cell._num_hidden:
                    neighbors = minefield.get_neighbors(cell.loc)
                    for n in neighbors:
                        ncell = minefield.cell_grid[n[0]][n[1]]
                        if ncell._status == cs.Cell_Status.COVERED:
                            ncell._status = cs.Cell_Status.MINE
                            cell._num_mine+=1
                if (8-cell._clue) - cell._num_safe == cell._num_hidden:
                    neighbors = minefield.get_neighbors(cell.loc)
                    for n in neighbors:
                        ncell = minefield.cell_grid[n[0]][n[1]]
                        if ncell._status == cs.Cell_Status.COVERED:
                            ncell._status = cs.Cell_Status.SAFE
                            cell._num_safe+=1
                            relevant.append(ncell)
    return(score)
