import pyglet
from pytmx.util_pyglet import load_pyglet
from player import Player
from monster import Monster
from npc import Npc
from container import Container

class Game:

  def __init__(self):
    
    self.player_name = None
    self.zone = None
    self.players = {}
    self.monsters = {}
    self.player_target = None
    self.spells = []
    self.npcs = {}
    self.containers = {}

    self.player_inventory = []

  def load(self, player_name, zone_source, players, monsters, npcs, containers):
    
    self.player_name = player_name
    self.zone = load_pyglet(zone_source)
    self.players = {}
    self.monsters = {}
    self.npcs = {}
    self.containers = {}
    self.offset = []

    for name,player in players.items():
      self.players[name] = Player(player['title'], player['gender'], player['body'], player['hairstyle'], player['haircolor'], player['armor'], player['head'], player['weapon'], player['x'], player['y'])

    for name,npc in npcs.items():
      self.npcs[name] = Npc(npc['title'], npc['gender'], npc['body'], npc['hairstyle'], npc['haircolor'], npc['armor'], npc['head'], npc['weapon'], npc['x'], npc['y'],npc['villan'])

    for name,monster in monsters.items():
      self.monsters[name] = Monster(monster['title'], monster['source'], monster['x'], monster['y'])
    
    for name,container in containers.items():
      self.containers[name] = Container(container['title'], container['x'], container['y'], container['source'], container['source_w'], container['source_h'], container['source_x'], container['source_y'])

    # Set our label to green :)
    self.players[player_name].label.color = (0,255,0,255)

  def draw(self):
    if self.player_name == None:
      return

    if not self.zone:
      return
    
    if self.players.has_key(self.player_name):
      self.offset = self.players[self.player_name].spritex - 320, self.players[self.player_name].spritey - 240
    
    for layer in self.zone.layers:
      if layer.name == 'character':

        for e in sorted( self.npcs.values() + self.monsters.values() + self.players.values() + self.containers.values(), key=lambda a: a.y, reverse=True):
          if e == self.player_target:
            e.draw(self.offset, True)
          else:
            e.draw(self.offset, False)

        for spell in self.spells:
          if not spell.expired:
            spell.draw(self.offset)

      if layer.name == 'blocked' or layer.name == 'block' or layer.name == 'spawns':
        # Don't draw the blocked layer
        pass
      else:
        
        for x, y, image in layer.tiles():
          y = self.zone.height - y - 1
          if x not in range(self.players[self.player_name].x - 30, self.players[self.player_name].x + 30):
            continue
          if y not in range(self.players[self.player_name].y - 30, self.players[self.player_name].y + 30):
            continue
          image.blit(x * self.zone.tilewidth - self.offset[0], y  * self.zone.tileheight - self.offset[1])

