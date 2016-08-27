import pyglet
from pytmx.util_pyglet import load_pyglet
from character import Character
from monster import Monster

class Game:

  def __init__(self):
    
    self.player_name = None
    self.zone = None
    self.players = {}
    self.monsters = {}
    self.player_target = None
  
  def load(self, player_name, zone_source, players, monsters):
    
    self.player_name = player_name
    self.zone = load_pyglet(zone_source)
    self.players = {}
    self.monsters = {}
    self.offset = []

    for name,player in players.items():
      self.players[name] = Character(player['title'], player['source'], player['x'], player['y'])

    for name,monster in monsters.items():
      self.monsters[name] = Monster(player['title'], monster['source'], monster['x'], monster['y'])

  def draw(self):
    
    if self.player_name == None:
      return

    if not self.zone:
      return

    self.offset = self.players[self.player_name].spritex - 320, self.players[self.player_name].spritey - 240
    
    for layer in self.zone.layers:
      if layer.name == 'character':
        
        for name,monster in self.monsters.items():
          target = False
          if name == self.player_target:
            target = True

          monster.draw(self.offset, target)
        
        for player in self.players.values():
          player.draw(self.offset)

      if layer.name == 'blocked' or layer.name == 'block':
        # Don't draw the blocked layer
        pass
      else:
        
        for x, y, image in layer.tiles():
          y = self.zone.height - y - 1
          if x not in range(self.players[self.player_name].x - 12, self.players[self.player_name].x + 12):
            continue
          if y not in range(self.players[self.player_name].y - 12, self.players[self.player_name].y + 12):
            continue
          image.blit(x * self.zone.tilewidth - self.offset[0], y  * self.zone.tileheight - self.offset[1])

