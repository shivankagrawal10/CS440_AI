import map as mp
import matrix_solver as ms
import constants
import numpy as np
import cell_status as cs

class agent:

    def __init__(self, minefield, strategy, starting_hints):
        self.minefield = minefield
        self.strategy = strategy
        self.map = mp.Map(minefield.dim, starting_hints)
        self.knowledge_base = None
        self.correct_uncovers = 0
        self.incorrect_uncovers = 0
        self.correct_flags = 0
        self.incorrect_flags = 0
        self.score = 0
        self.stop = 0

    def play_game(self):
        print("Starting Map:")
        self.map.print_map()
        while self.map.covered:
            input("Proceed")
            safes = set()
            mines = set()
            if self.strategy == constants.STRATEGY_1:
                self.strat_1(safes, mines)
            elif self.strategy == constants.STRATEGY_2:
                self.strat_2(safes, mines)
            if not safes and not mines:
                print('Random')
                random = self.randomchoice(self.map.covered)
                if self.minefield.field[random[0],random[1]] == 1:
                    mines.add(random)
                    self.stop = -1
                else:
                    self.score+=1+self.stop
                    safes.add(random)
            print("Predicted safe cells are", safes)
            print("Predicted mine cells are", mines)
            self.process_safe_preds(safes)
            self.process_mine_preds(mines)
            print("New map:")
            self.map.print_map()
        return(self.score)
    def strat_1(self, safes, mines):
        for coord in self.map.safes:
            cell = self.map.get_cell(coord)
            neighbors = self.map.get_neighbors(coord)
            if cell._clue - cell._num_mine == cell._num_hidden:
                for n in neighbors:
                    if n._status == cs.Cell_Status.COVERED:
                        mines.add(n.loc)
            if (len(neighbors) - cell._clue) - cell._num_safe == cell._num_hidden:
                for n in neighbors:
                    if n._status == cs.Cell_Status.COVERED:
                        safes.add(n.loc)
                        self.score+=1+self.stop

    def strat_2(self, safes, mines):
        knowledge_base = []
        for coord in self.map.safes:
            cell = self.map.get_cell(coord)
            if cell._num_hidden == 0:
                continue
            neighbors = self.map.get_neighbors(coord)
            b = cell._clue - cell._num_mine
            row = np.zeros((self.map.d * self.map.d) + 1)
            row[-1] = b
            for n in neighbors:
                if n._status == cs.Cell_Status.COVERED:
                    flat_index = n.loc[0] * self.map.d + n.loc[1]
                    row[flat_index] = 1
            knowledge_base.append(row)
        if not knowledge_base:
            return
        ms.matrixSolver(knowledge_base)
        for row in knowledge_base:
            max_val = 0
            min_val = 0
            pos_entries = set()
            neg_entries = set()
            for i in range(self.map.d * self.map.d):
                entry = row[i]
                two_d_coord = (i // self.map.d, i % self.map.d)
                if entry > 0:
                    max_val += entry
                    pos_entries.add(two_d_coord)
                elif entry < 0:
                    min_val += entry
                    neg_entries.add(two_d_coord)
            if max_val == row[-1]:
                for tup in pos_entries:
                    mines.add(tup)
                for tup in neg_entries:
                    safes.add(tup)
            elif min_val == row[-1]:
                for tup in pos_entries:
                    safes.add(tup)
                    self.score+=1+self.stop
                for tup in neg_entries:
                    mines.add(tup)

    def process_safe_preds(self, safes):
        for safe in safes:
            if safe not in self.map.covered:
                continue
            cell = self.map.get_cell(safe)
            is_safe = self.minefield.query(safe, constants.OPEN)
            if is_safe:
                cell._status = cs.Cell_Status.SAFE
                cell._clue = self.minefield.gen_clue(safe)
                self.correct_uncovers += 1
                self.map.safes.add(safe)
            else:
                cell._status = cs.Cell_Status.MINE
                self.incorrect_uncovers += 1
                self.map.mines.add(safe)
            self.map.covered.remove(safe)
            neighbors = self.map.get_neighbors(safe)
            for n in neighbors:
                n._num_hidden -= 1
                if cell._status == cs.Cell_Status.SAFE:
                    n._num_safe += 1
                elif cell._status == cs.Cell_Status.MINE:
                    n._num_mine += 1

    def process_mine_preds(self, mines):
        for mine in mines:
            if mine not in self.map.covered:
                continue
            cell = self.map.get_cell(mine)
            is_mine = self.minefield.query(mine, constants.BLOCKED)
            if is_mine:
                cell._status = cs.Cell_Status.MINE
                self.correct_flags += 1
                self.map.mines.add(mine)
            else:
                cell._status = cs.Cell_Status.SAFE
                self.incorrect_flags += 1
                self.map.safes.add(mine)
            self.map.covered.remove(mine)
            neighbors = self.map.get_neighbors(mine)
            for n in neighbors:
                n._num_hidden -= 1
                if cell._status == cs.Cell_Status.SAFE:
                    n._num_safe += 1
                elif cell._status == cs.Cell_Status.MINE:
                    n._num_mine += 1

    def randomchoice(self, my_set):
        selection = None
        index = None
        if len(my_set)-1 == 0:
            index = 0
        else:
            index = np.random.randint(0, high=(len(my_set)-1))
        i = 0
        for entry in my_set:
            if i == index:
                selection = entry
                break
            i += 1
        return selection
