import random
import time

class Spawn:

  def __init__(self, source, title, x, y, zone, spawn_max, hp, mp, hit, dam, arm, monster):

    print "Loading spawn %s" % title

    self.source = source
    self.title = title
    self.x = x
    self.y = y
    self.zone = zone
    self.monster = monster
    self.last_spawn = time.time()
    self.spawn_delay = 5
    self.spawn_max = spawn_max 
    self.spawn_count = 0

    self.stats = { 'mp': [mp,mp], 'hp': [hp,hp], 'hit': hit, 'dam': dam, 'arm': arm }

    self.nx = self.x
    self.ny = self.y

  def spawn(self, world):

    if time.time() - self.last_spawn > self.spawn_delay and self.spawn_count < self.spawn_max:
      world.add_monster(self.monster, self, self.source, self.title, self.nx, self.ny, self.zone, self)
      self.spawn_count += 1
      self.last_spawn = time.time()
      
      self.nx = random.randint(self.x - 2, self.x + 2)
      self.ny = random.randint(self.y - 2, self.y + 2)

