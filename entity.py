class Entity:
  def __init__(self):
    print('initing entity')
    self.token = DEFAULT_TOKEN
    self.age   = 1
    
  # todo overload == the real way
  def equals(self, other):
    return self.token == other.token and self.location.x == other.location.x and self.location.y == other.location.y
    
  def set_location(self, world, coordinate):
    self.world    = world
    self.location = coordinate
    world.add_object(self, coordinate)
  
  def get_older(self):
    self.age += 1
  
  def turn(self, world):
    pass