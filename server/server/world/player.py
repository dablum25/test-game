import time
import random
from twisted.internet import task, reactor

class Player:

  def __init__(self, name, title, gender, body, hairstyle, haircolor, password, x, y, zone, spells, hp, mp, hit, dam, arm, world):

    self.title = title
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone
    self.online = False
    self.password = password
    self.target = None
    self.fighting = False
    self.spells = spells # list of spells known by this player
    self.running = False
    self.hp = [ hp, hp ]
    self.mp = [ mp, mp ]
    self.hit = hit
    self.dam = dam
    self.arm = arm
    self.gold = 0
    self.mode = 'wait' # wait, running, fighting, casting, dead
    self.direction = 'south'
    self.world = world
    self.path = []
    self.gender = gender
    self.hairstyle = hairstyle
    self.haircolor = haircolor
    self.body = body

    # Triggers
    self.trigger_refresh = False
    self.trigger_statsupdate = False

    # Schedule update task
    self.update_task = task.LoopingCall(self.update)
    self.update_task.start(1.0)
    
    # Schedule pathfollow task
    self.pathfollow_task = task.LoopingCall(self.pathfollow)
    self.pathfollow_task.start(0.50)

  def state(self):
    
    armor = 'clothes'
    weapon = 'unarmed'
    head = 'none'
    # Get armor type
    for item in self.world.items.values():
      if item.player == self.name and item.equipped == 1:
        if item.slot == 'armor':
          armor = item.gear_type
        elif item.slot == 'weapon':
          weapon = item.gear_type
        elif item.slot == 'head':
          head = item.gear_type

    return { 'title': self.title,
             'name': self.name, 
             'gender': self.gender, 
             'body': self.body, 
             'hairstyle': self.hairstyle, 
             'haircolor': self.haircolor, 
             'armor': armor, 
             'head': head, 
             'weapon': weapon, 
             'x': self.x, 
             'y': self.y, 
             'zone': self.zone, }

  def take_damage(self, attacker, damage):

    if not self.target:
      self.target = attacker

    self.hp[0] -= damage
    print "DAMAGE!"
    self.trigger_statsupdate = True

  def pathfollow(self):
    
    if self.path:
      self.mode = 'running'
      dest = self.path.pop(0)
      
      if dest[0] > self.x:
        self.direction = 'east'
      elif dest[0] < self.x:
        self.direction = 'west'
      
      if dest[1] > self.y:
        self.direction = 'north'
      elif dest[1] < self.y:
        self.direction = 'south'  
      
      self.world.events.append({ 'type': 'playermove', 'name': self.name, 'zone': self.zone, 'direction': self.direction, 'start': (self.x,self.y), 'end': dest })
      
      self.x = dest[0]
      self.y = dest[1]
      
      # set mode to waiting if path is now empty
      if not self.path:
        self.mode = 'wait'

  def update(self):
    
    if not self.online:
      return

    if self.hp[0] < 1:
      if self.mode != 'dead':
        self.mode = 'dead'
        self.world.events.append({ 'type': 'playerdie', 'name': self.name, 'title': self.title, 'zone': self.zone })
        reactor.callLater(10.0, self.world.respawn_player, self)

    # Are we on a warp tile?
    for warp in self.world.warps:
      if warp.start_x == self.x and warp.start_y == self.y and warp.start_zone == self.zone:
        self.world.warp(self, warp)

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

    elif self.mode == 'fighting':
      
      if self.target is None:
        self.mode = 'wait'
        return
      
      if self.target.mode == 'dead':
        self.mode = 'wait'
        self.target = None
        return
      
      tohit  = random.randint(1,20) + self.world.get_player_hit(self.name)
      damage = random.randint(1, self.world.get_player_dam(self.name))
      attack = self.world.get_player_attack_type(self.name)

      if tohit >= self.target.arm:
        # It's a hit
        self.world.events.append({'type': 'player'+attack, 'name': self.name, 'dam': damage, 'target': self.target.name, 'zone': self.zone, 'target_title': self.target.title })
        self.target.take_damage(self,damage)

    elif self.mode == 'casting':
      pass
    
    elif self.mode == 'dead':
      pass


