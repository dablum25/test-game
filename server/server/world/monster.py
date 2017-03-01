import time
import random
import ConfigParser
from twisted.internet import task, reactor

class Monster:
  
  config = ConfigParser.RawConfigParser()
  config.read('data/monsters.ini')
  index = 0

  def getid(self):
    
    Monster.index += 1
    return Monster.index

  def __init__(self, name, x, y, zone, world, spawn):
    
    self.name   = "%s-%s" % (name, self.getid())
    self.world  = world
    self.x      = x
    self.y      = y
    self.zone   = zone
    self.spawn  = spawn

    self.title  = Monster.config.get(name,'title')
    self.level  = Monster.config.getint(name, 'level')
    self.source = Monster.config.get(name,'source')
    self.hp     = [ Monster.config.getint(name, 'hp'), Monster.config.getint(name,'hp') ]
    self.hit    = Monster.config.getint(name, 'hit')
    self.arm    = Monster.config.getint(name, 'dam')
    self.dam    = Monster.config.getint(name, 'arm')
    self.mode   = Monster.config.get(name, 'mode')
    self.loot   = Monster.config.get(name, 'loot')

    self.target = None


    self.update_task = task.LoopingCall(self.update)
    self.update_task.start(1.0)

    self.world.monsters[self.name] = self
    
    self.world.events.append({ 'type':   'addmonster', 
                               'source': self.source, 
                               'title':  self.title,
                               'name':   self.name, 
                               'x':      self.x, 
                               'y':      self.y, 
                               'zone':   self.zone })

  def state(self):

    return { 'title': self.title, 'source': self.source, 'name': self.name, 'x': self.x, 'y': self.y, 'zone': self.zone, }

  def take_damage(self, attacker, damage):

    if not self.target:
      self.target = attacker

    self.mode = 'fighting'
    self.hp[0] -= damage

  def update(self):
    # Are we dead:
    if self.hp[0] < 1:
      if self.mode != 'dead':
        self.mode = 'dead'
        self.world.events.append({ 'type': 'monsterdie', 'name': self.name, 'title': self.title, 'zone': self.zone })
        reactor.callLater(2.0, self.world.cleanup_monster, self)

    if self.mode == 'wait':
      # heal 10% per second while waiting
      if self.hp[0] < self.hp[1]:
        self.hp[0] += self.hp[1]/10
      # but dont go over!
      if self.hp[0] > self.hp[1]:
        self.hp[0] = self.hp[1]

    elif self.mode == 'wander':
      # 33% chance we wander
      #if random.choice([True, False, False]):
      #  return

      if random.random() > 0.10:
        return

      direction = 'south'
      x = random.randint(-1,1)
      y = 0
      if x > 0:
        direction = 'east'
      elif x < 0:
        direction = 'west'
      elif x == 0:
        y = random.randint(-1,1)
        if y > 0:
          direction = 'north'
        if y < 0:
          direction = 'south'
      
      if x == 0 and y == 0:
        return

      if not self.world.zones[self.zone].open_at(self.x + x, self.y + y):
        return
      
      self.world.events.append({'type': 'monstermove', 'name': self.name, 'zone': self.zone, 'direction': direction, 'start': (self.x,self.y), 'end': (self.x + x, self.y + y)})
      self.x += x
      self.y += y
    
    elif self.mode == 'fighting':
      print "fighting", self.target.name
      if self.target.mode == 'dead':
        self.mode = 'wait'
        self.target = None
      
      if not self.target:
        self.mode = 'wait'
        return
      
      tohit  = random.randint(1,20) + self.hit
      damage = random.randint(1, self.dam)

      player_arm = self.world.get_player_arm(self.target.name)

      if tohit >= player_arm:
        # It's a hit
        self.world.events.append({'type': 'monsterattack', 'name': self.name, 'dam': damage, 'target': self.target.name, 'zone': self.zone, 'title': self.title, 'target_title': self.target.title })
        self.target.take_damage(self,damage)
    
    elif self.mode == 'dead':
      pass

    elif self.mode == 'flee':
      pass
