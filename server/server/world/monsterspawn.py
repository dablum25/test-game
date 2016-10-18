import random
import time
import copy
import ConfigParser
from monster import Monster
from twisted.internet import task
import ConfigParser

class MonsterSpawn:

  monster_index = 0
  
  # Load monster from data/monsters.ini
  config = ConfigParser.RawConfigParser()
  config.read('data/monsters.ini')


  def __init__(self, name, x, y, w, h, zone, spawn_max, spawn_delay, world):

    self.monster_index += 1
    self.name = name
    self.source = self.config.get(name, 'source')
    self.title = self.config.get(name, 'title')
    self.mode = self.config.get(name, 'mode')
    self.x = x/32
    self.y = y/32
    self.w = w/32
    self.h = h/32
    self.zone = zone
    self.spawn_delay = spawn_delay
    self.spawn_max = spawn_max 
    self.spawn_count = 0
    self.world = world
    hp = self.config.getint(name, 'hp')
    self.hp = [ hp, hp ]
    self.mp = [ 0, 0 ]
    self.level = self.config.getint(name, 'level')
    self.hit   = self.config.getint(name, 'hit')
    self.arm   = self.config.getint(name, 'arm')
    self.dam   = self.config.getint(name, 'dam')

    # spawn, source, title, x, y, zone, hp, mp, hit, arm, dam
    self.build_hash = { 'source': self.source,
                        'title': self.title,
                        'mode': self.mode,
                        'zone': self.zone,
                        'hp': self.hp,
                        'mp': self.mp,
                        'hit': self.hit,
                        'dam': self.dam,
                        'arm': self.arm, }

    # Schedule update task
    self.spawn_task = task.LoopingCall(self.spawn)
    self.spawn_task.start(self.spawn_delay, now=False)
  
  def spawn(self):

    if self.spawn_count < self.spawn_max:
      name = "%s-%s" % (self.name, self.monster_index)
      self.monster_index += 1

      # Generate build hash and set a random spawn location within hash
      build = copy.deepcopy(self.build_hash)
      build['x'] = random.randint(self.x, self.x+self.w)
      build['y'] = random.randint(self.y, self.y+self.h)

      self.world.monsters[name] = Monster(name=name, world=self.world, spawn=self, **build)
      self.spawn_count += 1
      
      self.world.events.append({ 'type': 'addmonster', 
                                 'source': build['source'], 
                                 'title': build['title'], 
                                 'name': name, 
                                 'x': build['x'], 
                                 'y': build['y'], 
                                 'zone': build['zone'] })
