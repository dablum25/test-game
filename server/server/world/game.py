import time
import os,ConfigParser
import random

from spawn import Spawn
from player import Player
from monster import Monster
from zone import Zone
from spell import Spell
from container import Container
from item import Item

def d4roll(count):

  roll = 0
  for r in range(0, count):
    roll += random.randint(1,4)

  return roll

def d6roll(count=1):

  roll = 0
  for r in range(0, count):
    roll += random.randint(1,6)

  return roll


def d8roll(count=1):

  roll = 0
  for r in range(0, count):
    roll += random.randint(1,8)

  return roll


def d10roll(count=1):

  roll = 0
  for r in range(0, count):
    roll += random.randint(1,10)

  return roll


def d20roll(count=1):
  
  roll = 0
  for r in range(0, count):
    roll += random.randint(1,20)

  return roll


def dpRoll():

  return random.randint(1,100)


class Game:

  def __init__(self):
    # Players table
    self.players = {}

    # Monsters table
    self.monsters = {}
    self.monster_index = 0 # for randomly spawned monsters

    # Monster Spawn list
    self.spawns = []

    # Items table
    self.items = {}

    # Spells table
    self.spells = {}

    # Containers table
    self.containers = {}

    # Zones table
    self.zones = {}

    # Events queue
    self.events = []

    # Tick counter
    self.tick = time.time()

    # For logging events
    self.last_event = 0

  def process_data(self, player_name, data, protocol=None):
    
    send_now = None

    if data['action'] == 'walk':
      self.walk(player_name, data['direction'])
    
    elif data['action'] == 'attack':
      self.player_attack(player_name, data['target'])

    elif data['action'] == 'equip':
      self.player_equip(player_name, data['item'])

    elif data['action'] == 'unequip':
      self.player_unequip(player_name, data['item'])

    elif data['action'] == 'cast':
      self.player_cast(player_name, data['spell'])

    elif data['action'] == 'chat':
      self.chat(player_name, data['message'])
    
    elif data['action'] == 'disengage':
      self.player_disengage(player_name)

    elif data['action'] == 'inventory':
      send_now =  self.player_inventory(player_name)

    elif data['action'] == 'refresh':
      
      zone_name = self.players[player_name].zone
      zone_source = self.zones[zone_name].source

      send_now = { 'type': 'refresh', 'player_name': player_name, 'zone': zone_name, 'zone_source': zone_source, 'players': {}, 'monsters': {}, 'inventory': {}  }
      
      # Add players to send_now dataset
      for k,v in self.players.items():
        if v.zone == zone_name and v.online:
          send_now['players'][k] = v.state()
    
      # Add monsters to send_now dataset
      for k,v in self.monsters.items():
        if v.zone == zone_name:
          send_now['monsters'][k] = v.state()
    
      # Add inventory items to send_now dataset
      for k,v in self.items.items():
        if v.player == player_name:
          send_now['inventory'][k] = v.state()
    
    return send_now


  def get_events(self, player_name, upto):

    # Collect all events from the relevant zone    
    event_list = [ e for e in self.events[upto:] if e['zone'] in [ 'all', self.players[player_name].zone ] ]

    return { "type": "events", "events": event_list }

  def player_join(self, player_name):
   
    # New player data
    self.players[player_name].online = True
      
    # Add addplayer event
    event = { 'type': 'addplayer' }
    event.update(self.players[player_name].state())
    self.events.append(event)

    return player_name
  
  def add_monster(self, monster, spawn, source, title, x, y, zone, myspawn):
   
    # New player data
    name = "monster-%s" % self.monster_index
    self.monster_index += 1

    # Create monster 
    self.monsters[name] = monster(source, name, title, x, y, zone)
    self.monsters[name].spawn = myspawn

    # Add addmonster event
    self.events.append({ 'type': 'addmonster', 'source': source, 'title': title, 'name': name, 'x': x, 'y': y, 'zone': zone })

  def remove_monster(self, name):
    
    self.monsters[name].spawn.spawn_count -= 1
    del self.monsters[name]

  def player_leave(self, player_name):
      
    # Add dropplayer event
    self.events.append({ 'type': 'dropplayer', 'name': player_name, 'zone': self.players[player_name].zone })
    self.players[player_name].online = False
    
  def walk(self, player_name, direction):
    '''
    Player requests to go north.
    '''
    
    send_event = False
    zone = self.players[player_name].zone
    startx = self.players[player_name].x
    starty = self.players[player_name].y
    endx = self.players[player_name].x
    endy = self.players[player_name].y

    if direction == 'north':
      endy += 1
    elif direction == 'south':
      endy -= 1
    elif direction == 'east':
      endx += 1
    elif direction == 'west':
      endx -= 1

    # If player is free, then perform action
    if self.players[player_name].free():
      if self.zones[zone].open_at(endx,endy):
        self.players[player_name].free_at = time.time() + 1.0
        send_event = True

    if send_event:
      self.players[player_name].x = endx
      self.players[player_name].y = endy
      self.events.append({ 'type': 'playermove', 'name': player_name, 'zone': zone, 'direction': direction, 'start': (startx,starty), 'end': (endx,endy) })

  def chat(self, player_name, message):
    
    zone = self.players[player_name].zone
    self.events.append({ 'type': 'playerchat', 'name': player_name, 'zone':  zone, 'message': message })

  def player_attack(self, player_name, target):
    
    monster = self.monsters[target]
    player = self.players[player_name]
    monster.target = player
    player.target = monster
    player.fighting = True
    monster.fighting = True

  def player_equip(self, player_name, item_name):
    
    equip_made = False
    if self.items.has_key(item_name):
      if self.items[item_name].player == player_name:
        if self.items[item_name].slot != None:
          self.items[item_name].equipped = True
          equip_made = True

    if equip_made:
      for name,item in self.items.items():
        if name != item_name and item.player == player_name and item.slot == self.items[item_name].slot and item.equipped:
          item.equipped = False
    
  def player_unequip(self, player_name, item_name):

    if self.items.has_key(item_name):
      if self.items[item_name].player == player_name and self.items[item_name].equipped:
        self.items[item_name].equipped = False

  def player_inventory(self, player_name):
    
    # Return hash of player's items
    return { 'type': 'inventory', 'inventory': { k: v for k, in v in items.items() if v.player == player } }

  def player_disengage(self, player_name):
    
    # Player disengages and stops fighting
    self.players[player_name].fighting = False

  def player_cast(self, player_name, spell):
   
    # Can't cast if fighting 
    if self.players[player_name].fighting:
      return

    if spell in self.players[player_name].spells:
      print player_name,"casts",spell_name
      self.events.append({ 'type': 'playercast', 'name': player_name, 'zone':  zone, 'caster_anim': caster_anim, 'target': target, 'target_anim': target_anim })
      
  def get_player_dam(self, player_name):

    # base damage
    base_damage = self.players[player_name].stats['dam']
    weapon_damage = 0
    
    for item_name,item in self.items.items():
      if item.equipped and item.slot == 'weapon' and item.player == player_name:
        weapon_damage = item.stats['dam']
    
    print base_damage,weapon_damage
    return base_damage + weapon_damage

  def loop(self):
    
    # Update game world
    for ms in self.spawns:
      ms.spawn(self)

    for name,monster in self.monsters.items():
      # Make monsters wander
      if monster.free():
        if monster.target == None:
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
            continue
          
          # Don't wanter more than 10 spaces
          #if abs(monster.x - x) > 10:
          #  continue

          #if abs(monster.y - y) > 10:
          #  continue

          monster.free_at = time.time() + 1.0
          self.events.append({'type': 'monstermove', 'name': name, 'zone': monster.zone, 'direction': direction, 'start': (monster.x,monster.y), 'end': (monster.x + x, monster.y + y)})
          monster.x += x
          monster.y += y
    
    # Update battles
    for name, player in self.players.items():
      if player.free() and player.target and player.fighting:
        player.free_at = time.time() + 1.0
        player_tohit = player.stats['hit']
        player_dam = self.get_player_dam(name)

        for weapon in self.items.values():
          if weapon.slot == 'weapon' and weapon.player == name and weapon.equipped:
            player_dam = weapon.stats['dam']
        
        monster_arm = player.target.stats['arm']

        # RULES
        # hit succeeds if d20 + player_tohit > monster_arm
        # d20 roll of 1 always failure
        # d20 roll of 20 always hit
        # damage = d<player damage>
        hitroll = random.randint(0,20) + player_tohit
        hit_succeeds = False
        if hitroll == 1:
          pass # miss
        elif hitroll >= 20:
          # hit
          hit_succeeds = True
        elif hitroll > monster_arm:
          # hit
          hit_succeeds = True
        
        hit_damage = 0
        if hit_succeeds:
          hit_damage = random.randint(0,player_dam)
          player.target.stats['hp'][0] -= hit_damage
        
        self.events.append({ 'type': 'playerslash', 'name': name, 'zone': player.zone, 'dam': hit_damage, 'target': player.target.title })
        
        # Are we dead?
        if player.stats['hp'][0] <= 0:
          self.events.append({ 'type': 'playerdie', 'name': name, 'zone': player.zone })
       
          # Free player after 5 seconds
          player.free_at = time.time() + 5
          
          # TODO:
          # - respawn player
        
        # if target gone, reset to none
        if player.target.name not in self.monsters.keys():
          player.target = None
          self.events.append({'type': 'playerstop', 'name': name})
             
    for name, monster in self.monsters.items():
      if monster.free() and monster.target and monster.fighting:
        monster.free_at = time.time() + 1.0
        monster_tohit = monster.stats['hit']
        monster_dam = monster.stats['dam']
        player_arm = monster.target.stats['arm']
        
        hitroll = random.randint(0,20) + monster_tohit
        hit_succeeds = False
        if hitroll == 1:
          pass # miss
        elif hitroll == 20:
          # hit
          hit_succeeds = True
        elif hitroll > player_arm:
          # hit
          hit_succeeds = True

        hit_damage = 0
        if hit_succeeds:
          hit_damage = random.randint(0,monster_dam)
          monster.target.stats['hp'][0] -= hit_damage
        
        self.events.append({ 'type': 'monsterattack', 'name': name, 'zone': monster.zone, 'dam': hit_damage, 'target': monster.target.title })
        
        # Are we dead?
        if monster.stats['hp'][0] <= 0:
          self.events.append({ 'type': 'monsterdie', 'name': name, 'zone': monster.zone })
          monster.spawn.spawn_count -= 1

          for p in self.players.values():
            if p.target == monster:
              p.target = None

          del self.monsters[name]
          
          # TODO:
          # - monster drops stuff
          # - player gains xp
       
       
    # Keepalive tick
    #if time.time() - 60 > self.tick:
    #  self.events.append({ 'type': 'tick', 'time': time.time(), 'zone': 'all' })
    #  self.tick = time.time()
    
    # Follow event queue
    for e in self.events[self.last_event:]:
      print "Event:", e

    self.last_event = len(self.events)

  def load_zones(self):

    zone_config = ConfigParser.RawConfigParser()
    zone_config.read('data/zones.ini')
    
    for zone in zone_config.sections():
      
      values = {}
      values['name'] = zone
      values['source'] = zone_config.get(zone,'source')
      values['title']  = zone_config.get(zone,'title')

      self.zones[zone] = Zone(**values)

  def load_players(self):
    
    player_config = ConfigParser.RawConfigParser()
    player_config.read('data/players.ini')

    for player in player_config.sections():
      
      values             = {}
      values['source']   = player_config.get(player,'source')
      values['zone']     = player_config.get(player,'zone')
      values['title']    = player_config.get(player,'title')
      values['x']        = player_config.getint(player,'x')
      values['y']        = player_config.getint(player,'y')
      values['password'] = player_config.get(player,'password')
      values['spells']   = player_config.get(player,'spells').split(',')
      values['hp']       = player_config.getint(player,'hp')
      values['mp']       = player_config.getint(player,'mp')
      values['hit']      = player_config.getint(player,'hit')
      values['dam']      = player_config.getint(player,'dam')
      values['arm']      = player_config.getint(player,'arm')
      values['name']     = player

      self.players[player] = Player(**values)

  def load_spawns(self):
    
    spawn_config = ConfigParser.RawConfigParser()
    spawn_config.read('data/spawns.ini')

    for spawn in spawn_config.sections():
      
      values              = {}
      values['source']    = spawn_config.get(spawn,'source')
      values['zone']      = spawn_config.get(spawn,'zone')
      values['title']     = spawn_config.get(spawn,'title')
      values['x']         = spawn_config.getint(spawn,'x')
      values['y']         = spawn_config.getint(spawn,'y')
      values['hp']        = spawn_config.getint(spawn,'hp')
      values['mp']        = spawn_config.getint(spawn,'mp')
      values['hit']       = spawn_config.getint(spawn,'hit')
      values['dam']       = spawn_config.getint(spawn,'dam')
      values['arm']       = spawn_config.getint(spawn,'arm')
      values['spawn_max'] = spawn_config.getint(spawn,'spawn_max')
      values['monster']   = Monster
       
      self.spawns.append(Spawn(**values))
  
  def load_items(self):
    
    item_config = ConfigParser.RawConfigParser()
    item_config.read('data/items.ini')

    for item in item_config.sections():
      
      values              = {}
      values['source']    = item_config.get(item,'source')
      values['player']    = item_config.get(item,'player')
      values['container'] = item_config.get(item,'container')
      values['title']     = item_config.get(item,'title')
      values['hit']       = item_config.getint(item,'hit')
      values['dam']       = item_config.getint(item,'dam')
      values['arm']       = item_config.getint(item,'arm')
      values['slot']      = item_config.get(item,'slot')
      values['name']      = item

      self.items[item] = Item(**values)

  def load_spells(self):

    spell_config = ConfigParser.RawConfigParser()
    spell_config.read('data/spells.ini')

    for spell in spell_config.sections():
      
      values          = {}
      values['name']  = spell
      values['title'] = spell_config.get(spell,'title')
      
      self.spells[spell] = Spell(**values)

  def load_containers(self):
    
    container_config = ConfigParser.RawConfigParser()
    container_config.read('data/containers.ini')

    for container in container_config.sections():
      
      values          = {}
      values['name']  = container
      values['title'] = container_config.get(container,'title')
      values['zone'] = container_config.get(container,'zone')
      values['x'] = container_config.getint(container,'x')
      values['y'] = container_config.getint(container,'y')
      
      self.containers[container] = Container(**values)

