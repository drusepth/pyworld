from entity import Entity

# Sapling configuration
SAPLING_SPAWN_CHANCE       = 0.05 # Chance to spawn on a tile never seen before
SAPLING_FRAMES_TO_MATURITY = 100  # Point at which this sapling becomes a full-grown tree
SAPLING_TOKEN              = 't'

# Tree configuration
TREE_SPAWN_CHANCE     = 0.001  # Chance to spawn a fully-grown tree
TREE_FRAMES_PER_BLOOM = 50     # Bloom fruit every this-many frames
TREE_MAX_AGE          = 1000   # Maximum age for a tree before it dies
TREE_TOKEN            = 'T'

# Fruit configuration
FRUIT_AGE_TO_ROT       = 30   # Age at which fruit becomes rotten
FRUIT_AGE_TO_DECOMPOSE = 80   # Age at which fruit disappears into fertilizer
FRUIT_TOKEN            = 'o'

class Sapling (Entity):
  def __init__(self):
    self.token = SAPLING_TOKEN
    
    # remove after super() calls
    self.age = 1
  
  def turn(self, world):
    # Grow up!
    if self.age >= SAPLING_FRAMES_TO_MATURITY:
      # Remove this sapling
      world.remove_object(self)
      
      # And spawn a grown tree in its place
      Tree().set_location(world, self.location)
      
      # todo deconstruct object for memory saving
    
class Tree (Entity):
  def __init__(self):
    self.token = TREE_TOKEN
    self.age   = SAPLING_FRAMES_TO_MATURITY # continue age from sapling
    
  def turn(self, world):
    # Aging
    if self.age > TREE_MAX_AGE:
      world.remove_object(self) # RIP
    
    # Bearing of fruit
    if self.age % TREE_FRAMES_PER_BLOOM == 0:
      Fruit().set_location(world, self.location)

class Fruit (Entity):
  def __init__(self):
    self.token  = FRUIT_TOKEN
    self.age    = 1
    self.rotten = False
  
  def turn(self, world):
    if self.age > FRUIT_AGE_TO_ROT:
      self.rotten = True
    
    if self.age > FRUIT_AGE_TO_DECOMPOSE:
      world.remove_object(self) # RIP
      if rng.random() < SAPLING_SPAWN_CHANCE:
        Sapling().set_location(world, self.location)
      
      # todo deconstruct object