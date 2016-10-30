import random
from Queue import Queue
from aenum import Enum

class Grid:

  # grid indexed from 0

  def __init__ (self, order):
    self.order = order
    self.size = self.order ** 2
    self.cells = [Cell(i) for i in range(self.size)]
    self.end = False
    self.blasted = False
    self.escaped = False
    self.marked = []
    self.revealer = GridRevealer(self)
    self.mines = []
    self.place_mines()


  def place_mines (self):
    self.mines = random.sample(xrange(self.size), self.order)
    for pos in self.mines:
      self.cells[pos].set_mine()
      self.set_count_cells(self.cells[pos])

  def set_count_cells (self, mine):
    if mine.is_mine():
      adj_cells = self.get_adj_cells(mine)
      for cell in adj_cells:
        if not cell.is_mine():
          cell.incr_count()

  def move (self, pos):
    if self.cells[pos].is_mine() and not self.end:
      self.end = True
      self.blasted = True
      self.cells[pos].reveal = True
    elif self.cells[pos].is_blank():
      self.reveal(self.cells[pos])
    else:
      self.cells[pos].reveal = True

  def mark (self, pos):
    if not self.cells[pos].reveal and not self.cells[pos].marked and self.is_valid_position(pos):
      self.marked.append(pos)
      self.cells[pos].marked = True
    if len(self.marked) > self.order:
      print "Already reached mark limit. Do something else!"
      return

  def show (self):
    for i in xrange(1,self.size+1):
      if not self.cells[i-1].reveal:
        if self.cells[i-1].marked:
          print "*",
        else:
          print "#",
      elif self.cells[i-1].is_mine():
        print "$",
      elif self.cells[i-1].is_blank():
        print "-",
      else:
        print self.cells[i-1].count,
      if i % 10 == 0 and i != 0:
        print "\n"

  def reveal (self, cell):
    if cell.is_mine():
      cell.reveal = True
      self.end = True
      return
    elif cell.is_blank():
      self.revealer.reset()
      self.revealer.reveal(cell)
    else:
      cell.reveal = True
      return

  def get_adj_positions (self, position):
    # "left, right, up, down, tl, tr, br, bl"
    if self.is_top_left(position):
      return "01010010"
    elif self.is_top_right(position):
      return "10010001"
    elif self.is_bottom_left(position):
      return "01100100"
    elif self.is_bottom_right(position):
      return "10101000"
    elif self.in_first_row(position):
      return "11010011"
    elif self.in_last_row(position):
      return "11101100"
    elif self.in_first_column(position):
      return "01110110"
    elif self.in_last_column(position):
      return "10111001"
    else:
      return "11111111"

  def get_adj_cells (self, cell):
    adj_positions = [cell.position - 1,
                     cell.position + 1,
                     cell.position - self.order,
                     cell.position + self.order,
                     cell.position - (self.order + 1),
                     cell.position - (self.order - 1),
                     cell.position + (self.order + 1),
                     cell.position + (self.order -1)]

    pos_str = self.get_adj_positions(cell.position)
    adj_cells = []
    for idx,i in enumerate(pos_str):
      if i == "1":
        adj_cells.append(self.cells[adj_positions[idx]])
    return adj_cells

  def is_valid_position (self, position):
    return position >= 0 and position <= self.size-1

  def is_cell_in_grid (self, cell):
    return is_valid_position(cell.position)

  def is_edge_position (self, position):
    return in_first_row(position) and in_last_row(position) and in_first_column(position) and in_last_column(position)

  def in_first_row (self, position):
    return position >= 0 and position <= self.order-1

  def in_last_row (self, position):
    return position <= self.size-1 and position >= self.size-self.order

  def in_first_column (self, position):
    return position % self.order == 0

  def in_last_column (self, position):
    return (position+1) % self.order == 0 and position != 0

  def is_top_left (self, position):
    return position == 0

  def is_top_right (self, position):
    return position == self.order - 1

  def is_bottom_left (self, position):
    return position == self.size - 1 - (self.order - 1)

  def is_bottom_right (self, position):
    return position == self.size - 1

class GridRevealer:

  def __init__ (self, grid):
    self.grid = grid
    self.queue = Queue()
    self.visited = {}

  def reset (self):
    self.queue = Queue()
    self.visited = {}

  def reveal (self, cell):
    if cell.is_blank():
      # bfs ftw
      self.queue.put(cell)
      self.visited[cell] = True
      while not self.queue.empty():
        j = self.queue.get(cell)
        j.reveal = True
        for i in self.grid.get_adj_cells(j):
          if not self.visited.has_key(i) or not self.visited[i]:
            self.visited[i] = True
            if i.is_blank():
              self.queue.put(i)
    else:
      cell.reveal = True
      return

class Cell:

  # cell types : 0 - mine, 1 - number, 2 - blank

  def __init__ (self,  position):
    self.type = 2
    self.count = 0
    self.position = position
    self.reveal = False
    self.marked = False

  def set_type (self, cell_type):
    self.type = cell_type

  def set_count (self, count):
    self.count = count
    self.type = 1

  def incr_count (self):
    self.count += 1
    self.type = 1

  def set_mine (self):
    self.type = 0
    self.count = None

  def is_mine (self):
    return self.type == 0

  def is_blank (self):
    return self.type == 2

  def mark (self):
    self.marked = True

  def show (self):
    print str(self.type) + " -- " + str(self.count)
