import random as rng

from entity import Entity
from coordinate import Coordinate

CREATURE_X_MOVEMENT_CHANCE = 0.5 # Chance to move left/right (each rolls separately)
CREATURE_Y_MOVEMENT_CHANCE = 0.5 # Chance to move up/down (each rolls separately)
CREATURE_MOVEMENT_RATE     = 1   # Number of tiles moved in the chosen direction
CREATURE_TOKEN             = 'C'

class Creature (Entity):
  def __init__(self):
    self.token = CREATURE_TOKEN
    
    # #todo call parent init
    # remove after super() call
    self.age = 1
  
  def turn(self, world):
    # Do random movement
    self.move_randomly(world)
    
    # Interact with stuff
    # #todo
  
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