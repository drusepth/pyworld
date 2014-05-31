# Brace for the java
import random as rng

# Our classes
from coordinate import Coordinate
from entity import Entity
from creature import Creature
from tree import *
from world import World

# Display configuration
VISION_WIDTH = 30   # Width of "nearby" 2D map to print out, in tiles
VISION_HEIGHT = 10  # Height of "nearby" 2D map to print out

# Main
world    = World()      # Create an infinite world to live in
creature = Creature()   # And create a creature to watch in it

# Add the creature to the world at (0, 0)
creature.set_location(world, Coordinate(0, 0))

while True:
  world.update()
  world.print2d(creature, VISION_WIDTH, VISION_HEIGHT)
  
  # Let the viewer progress turn-by-turn
  input()