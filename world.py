from coordinate import Coordinate
from tree import *

import random as rng

EMPTY_SPACE   = '-'
DEFAULT_TOKEN = '?'

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
    
  def objects_at(self, coordinate):
    # until coordinate comparison lel
    for coord in self.map.keys():
      if coord.equals(coordinate):
        return self.map[coord]
  
  def print2d(self, center_object, width, height):
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