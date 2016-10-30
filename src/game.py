import os
from mines import Grid

grid = Grid(10)
os.system("clear")
grid.show()
while not grid.end:
  c = raw_input(">")
  if c.startswith("#"):
    grid.mark(int(c[1:]))
  else:
    grid.move(int(c))
  os.system("clear")
  grid.show()
