import random
import time
import copy

class Spawn:

  def __init__(self, name, source, title, x, y, zone, spawn_max, hp, mp, hit, dam, arm):

    self.name = name
    self.source = source
    self.title = title
    self.x = x
    self.y = y
    self.zone = zone
    self.last_spawn = time.time()
    self.spawn_delay = 5
    self.spawn_max = spawn_max 
    self.spawn_count = 0

    self.hp = [ hp, hp ]
    self.mp = [ mp, mp ]
    self.hit = hit
    self.arm = arm
    self.dam = dam
    # spawn, source, title, x, y, zone, hp, mp, hit, arm, dam
    self.build_hash = { 'source': self.source,
                        'title': self.title,
                        'x': self.x,
                        'y': self.y,
                        'zone': self.zone,
                        'hp': self.hp,
                        'mp': self.dam,
                        'hit': self.hit,
                        'dam': self.dam,
                        'arm': self.arm, }

  def spawn(self, world):

    if time.time() - self.last_spawn > self.spawn_delay and self.spawn_count < self.spawn_max:
      world.add_monster(spawn=self, **copy.deepcopy(self.build_hash) )
      self.spawn_count += 1
      self.last_spawn = time.time()

