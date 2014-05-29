# Brace for the java
import random as rng

# Display configuration
MAP_WIDTH = 30
MAP_HEIGHT = 10

# Creature configuration
CREATURE_X_MOVEMENT_CHANCE = 0.5 # Chance to move left/right (each rolls separately)
CREATURE_Y_MOVEMENT_CHANCE = 0.5 # Chance to move up/down (each rolls separately)
CREATURE_MOVEMENT_RATE     = 1   # Number of tiles moved in the chosen direction

# Sapling configuration
SAPLING_SPAWN_CHANCE       = 0.05 # Chance to spawn on a tile never seen before
SAPLING_FRAMES_TO_MATURITY = 100  # Point at which this sapling becomes a full-grown tree

# Tree configuration
TREE_SPAWN_CHANCE     = 0.001  # Chance to spawn a fully-grown tree
TREE_FRAMES_PER_BLOOM = 50     # Bloom fruit every this-many frames
TREE_MAX_AGE          = 1000   # Maximum age for a tree before it dies

# Fruit configuration
FRUIT_AGE_TO_ROT = 30       # Age at which fruit becomes rotten
FRUIT_AGE_TO_DECOMPOSE = 80 # Age at which fruit disappears into fertilizer

# World Tokens
EMPTY_SPACE   = '-'
DEFAULT_TOKEN = '?'

# Entity Tokens
CREATURE_TOKEN = 'C'
SAPLING_TOKEN  = 't'
TREE_TOKEN     = 'T'
FRUIT_TOKEN    = 'o'

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  # todo real overloading of ==
  def equals(self, other_coordinate):
    return self.x == other_coordinate.x and self.y == other_coordinate.y
  
class World:
  def __init__(self):
    self.map = {}
    self.objects = [] # todo should probably be implemented as LRU cache

  def update(self):
    print(len(self.objects), 'objects in scope')
  
    # Deep copy self.objects because we can modify it by movement
    objects_to_update = []
    for o in self.objects:
      objects_to_update.append(o)
    
    for object in objects_to_update:
      object.turn(self)
      object.get_older()
    return True
  
  def randomize_tile(self, coordinate):
    # todo randomly shuffle options before rolling for each
    if rng.random() < SAPLING_SPAWN_CHANCE:
      Sapling().set_location(self, coordinate)
    elif rng.random() < TREE_SPAWN_CHANCE:
      Tree().set_location(self, coordinate)
    else:
      self.map[coordinate] = []
  
  def add_object(self, object, coordinate):
    self.objects.append(object)
    try: #todo just check if it exists with comparison operator
      self.map[coordinate].append(object)
    except KeyError:
      self.map[coordinate] = []
      self.map[coordinate].append(object)
  
  def remove_object(self, object):
    # Remove object from coordinate lookup # todo redo with == overloaded
    for coord in self.map.keys():
      if coord.equals(object.location):
        for obj in self.map[coord]:
          if object.equals(obj):
            self.map[coord].remove(obj)
    
    # Remove object from self.objects index
    for obj in self.objects:
      if object.equals(obj):
        self.objects.remove(obj)
  
  def move_object(self, object, destination):
    current_location = Coordinate(object.location.x, object.location.y)
    self.remove_object(object)
    self.add_object(object, destination)
    object.location = Coordinate(destination.x, destination.y)
  
  def print(self, center_object, width, height):
    camera_center = center_object.location
    print ('printing world centered at (', camera_center.x, ',', camera_center.y, ')')
    for y in range(camera_center.y - int(height / 2), 1 + camera_center.y + int(height / 2)):
      line = [] # until I can figure out how to print without a \n    
      for x in range(camera_center.x - int(width / 2), 1 + camera_center.x + int(width / 2)):
        here = Coordinate(x, y)

        # short circuit until I can override comparison operator
        for coord in self.map.keys():
          if coord.equals(here):
            here = coord
            break

        if here in self.map.keys():
          tile_contents = self.map[here]
          if len(tile_contents) > 0:
            # If there are multiple things on the tile, show who was there first
            line.append(self.map[here][0].token) # || EMPTY_SPACE
          else:
            line.append(EMPTY_SPACE)
        else:
          # Never seen this tile before --> create it!
          self.randomize_tile(here)
          try:
            line.append(self.map[here][0].token)
          except IndexError:
            line.append(EMPTY_SPACE)
          except KeyError:
            line.append(EMPTY_SPACE)
            
      # Manually join each element until I can look up python join() syntax
      to_print = ''
      for tile in line:
        to_print += tile + ' '
      line = to_print
      
      print(line)
    
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

class Creature (Entity):
  def __init__(self):
    self.token = CREATURE_TOKEN
    
    # #todo call parent init
    # remove after super() call
    self.age = 1
  
  def turn(self, world):
    # Do random movement
    self.move_randomly(world)
  
  def move_randomly(self, world):
    # Mutate destination +/- 1 in x/y coordinates to move randomly
    destination = Coordinate(self.location.x, self.location.y)
    if rng.random() < CREATURE_X_MOVEMENT_CHANCE:
      destination.x += CREATURE_MOVEMENT_RATE
    elif rng.random() < CREATURE_X_MOVEMENT_CHANCE:
      destination.x -= CREATURE_MOVEMENT_RATE
    
    if rng.random() < CREATURE_Y_MOVEMENT_CHANCE:
      destination.y += CREATURE_MOVEMENT_RATE
    elif rng.random() < CREATURE_Y_MOVEMENT_CHANCE:
      destination.y -= CREATURE_MOVEMENT_RATE

    world.move_object(self, destination)

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
    
# Main
world    = World()      # Create an infinite world to live in
creature = Creature()   # And create a creature to watch in it

# Add the creature to the world at (0, 0)
creature.set_location(world, Coordinate(0, 0))

while True:
  world.update()
  world.print(creature, MAP_WIDTH, MAP_HEIGHT)
  
  # Let the viewer progress turn-by-turn
  input()