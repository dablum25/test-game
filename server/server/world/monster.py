import time
import random
from twisted.internet import task, reactor

class Monster:

  def __init__(self, source, name, title, x, y, zone, hp, mp, hit, dam, arm, world):
    
    self.source = source
    self.title = title
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone
    self.spawn = None
    
    self.hp = hp
    self.mp = mp
    self.hit = hit
    self.dam = dam
    self.arm = arm

    self.world = world
    self.mode = 'wait' # wander, fight, flee, wait, dead
    self.target = None

    self.update_task = task.LoopingCall(self.update)
    self.update_task.start(1.0)

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
      if self.mp[0] < self.mp[1]:
        self.mp[0] += self.mp[1]/10
      # but dont go over!
      if self.hp[0] > self.hp[1]:
        self.hp[0] = self.hp[1]
      if self.mp[0] > self.mp[1]:
        self.mp[0] = self.mp[1]

    elif self.mode == 'wander':
      
      # 50% chance we wander
      if random.choice([True, False]):
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
