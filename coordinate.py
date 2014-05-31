class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  # todo real overloading of ==
  def equals(self, other_coordinate):
    return self.x == other_coordinate.x and self.y == other_coordinate.y