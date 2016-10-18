import time
import random
from twisted.internet import task, reactor

class Npc:

  def __init__(self, name, title, gender, body, hairstyle, haircolor, armor, head, weapon, x, y, zone, hp, mp, hit, dam, arm, shop, quest, villan, world, spawn=None):

    self.title = title
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone
    self.free_at = time.time()
    self.target = None
    self.fighting = False
    self.running = False
    self.hp = hp
    self.mp = hp 
    self.hit = hit
    self.dam = dam
    self.arm = arm
    self.world = world
    self.gender = gender
    self.body = body
    self.hairstyle = hairstyle
    self.haircolor = haircolor
    self.armor = armor
    self.head = head
    self.weapon = weapon
    self.attack_type = 'slash'
    
    if self.weapon in [ 'sword', 'wand' ]:
      self.attack_type = 'slash'
    elif self.weapon in [ 'spear' ]:
      self.attack_type = 'thrust'
    elif self.weapon in [ 'bow' ]:
      self.attack_type = 'shoot'

    self.spawn = spawn

    # Merchant shop
    self.shop = shop

    # Quest info
    self.quest = quest

    if self.shop or self.quest:
      self.mode = 'wait'
    else:
      self.mode = 'wander'


    # bad guy
    self.villan = villan

    self.update_task = task.LoopingCall(self.update)
    self.update_task.start(1.0)
    
  def state(self):
    
    return { 'title': self.title,
             'name': self.name, 
             'gender': self.gender, 
             'body': self.body, 
             'hairstyle': self.hairstyle,
             'haircolor': self.haircolor,
             'armor': self.armor,
             'head': self.head,
             'weapon': self.weapon,
             'x': self.x, 
             'y': self.y, 
             'zone': self.zone,
             'villan': self.villan, }
  
  def take_damage(self, attacker, damage):

    if not self.target:
      self.target = attacker
    print self.hp[0], damage
    self.mode = 'fighting'
    self.hp[0] -= damage


  def update(self):
    # Are we dead:
    if self.hp[0] < 1:
      if self.mode != 'dead':
        self.mode = 'dead'
        self.world.events.append({ 'type': 'npcdie', 'name': self.name, 'title': self.title, 'zone': self.zone })
        reactor.callLater(10.0, self.world.cleanup_npc, self)

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
      
      self.world.events.append({'type': 'npcmove', 'name': self.name, 'zone': self.zone, 'direction': direction, 'start': (self.x,self.y), 'end': (self.x + x, self.y + y)})
      self.x += x
      self.y += y
    
    elif self.mode == 'fighting':

      if not self.target:
        self.mode = 'wait'
        return
      
      if self.target.mode == 'dead':
        self.mode = 'wait'
        self.target = None
        return
    
      if not self.world.in_attack_range(self,self.target):
        # TODO: get path to target and move close enough to attack
        return
      
      tohit  = random.randint(1,20) + self.hit
      damage = random.randint(1, self.dam)
      arm    = 0
      
      if self.target.__class__.__name__ == 'Player':
        arm = self.world.get_player_arm(self.target.name)
      else:
        arm = self.target.arm

      if tohit >= arm:
        # It's a hit
        self.world.events.append({'type': 'npc'+self.attack_type, 'name': self.name, 'dam': damage, 'target': self.target.name, 'zone': self.zone, 'title': self.title, 'target_title': self.target.title })
        self.target.take_damage(self,damage)
    
    elif self.mode == 'dead':
      pass

    elif self.mode == 'flee':
      pass
