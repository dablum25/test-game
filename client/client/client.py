import pyglet
from pytmx.util_pyglet import load_pyglet
import pygletreactor
pygletreactor.install() # <- this must come before...
from twisted.internet import reactor, task # <- ...importing this reactor!

from ui import LoginManager,ConnectManager,ChatWindowManager
from net import GameClientFactory,GameClientProtocol
from game.game import Game
from game.monster import Monster

class Client:

  def __init__(self):

    self.window = pyglet.window.Window()
    self.loginManager = LoginManager(self)
    self.connectManager = ConnectManager(self)
    self.chatManager = ChatWindowManager(self)
    self.factory = GameClientFactory(self)
    self.protocol = None
    self.game = Game()

  def process(self, data):
    print data
    if data['type'] == 'events':
      for event in data['events']:
        self.process(event)
    elif data['type'] == 'loginsucceeded':
      self.play() # OK, we can switch to playing mode
      print data
    elif data['type'] == 'refresh':
      self.game.load(data['player_name'],data['zone_source'],data['players'],data['monsters'])
      print data
    elif data['type'] == 'addplayer':
      self.game.players[data['name']] = Character(data['title'],data['source'],data['x'],data['y'])
      message = "%s is here." % (data['name'])
      self.chatManager.add_message(message)
      print data
    elif data['type'] == 'dropplayer':
      message = "%s left." % (data['name'])
      self.chatManager.add_message(message)
      print data
    elif data['type'] == 'addmonster':
      self.game.monsters[data['name']] = Monster(data['title'],data['source'],data['x'],data['y'])
      print data
    elif data['type'] == 'playermove':
      if self.game.players.has_key(data['name']):
        self.game.players[data['name']].go(data['direction'],data['start'])
      print data
    elif data['type'] == 'monstermove':
      if self.game.monsters.has_key(data['name']):
        self.game.monsters[data['name']].go(data['direction'],data['start'])
      print data
    elif data['type'] == 'playerstop':
      if self.game.players.has_key(data['name']):
        self.game.players[data['name']].wait()
      print data
    elif data['type'] == 'playerslash':
      if self.game.players.has_key(data['name']):
        self.game.players[data['name']].slash()
        title = self.game.players[data['name']].title
        dam = data['dam']
        target = data['target']
        self.chatManager.add_message("%s hits %s for %s damage!" % (title,target,dam))
      print data
    elif data['type'] == 'playerthrust':
      print data
    elif data['type'] == 'playerbow':
      print data
    elif data['type'] == 'playercast':
      print data
    elif data['type'] == 'playerdie':
      if self.game.players.has_key(data['name']):
        self.game.players[data['name']].die()
      print data
    elif data['type'] == 'monsterattack':
      if self.game.monsters.has_key(data['name']):
        title = self.game.monsters[data['name']].title
        dam = data['dam']
        target = data['target']
        self.chatManager.add_message("%s hits %s for %s damage!" % (title,target,dam))
      print data
    elif data['type'] == 'monsterdie':
      if self.game.monsters.has_key(data['name']):
        del self.game.monsters[data['name']]
        # if this monster was the player's target, reset target and tell player to wait
        if data['name'] == self.game.player_target:
          self.game.player_target = None
    elif data['type'] == 'playerchat':
      message = "<%s> %s" % (data['name'],data['message'])
      self.chatManager.add_message(message)
      print data
    elif data['type'] == 'tick':
      print data
    elif data['type'] == 'loginfailed':
      print data

  def set_protocol(self, protocol):
    
    self.protocol = protocol

  def try_connect(self, server, port):
 
    reactor.connectTCP(server, port, self.factory)

  def connected(self):

    self.login()

  def login(self):
    
    self.connectManager.delete()
    
    @self.window.event
    def on_draw():
      self.window.clear()
      self.loginManager.draw()

  def try_login(self, username, password):

    # Send login request
    self.protocol.send({"action": "login","name": username, "password": password})
    
  def chat(self, message):
    self.protocol.send({"action": "chat", "message": message})
       
  def command(self, command):
  
    if command[0] == 'logout':
      self.logout()

    elif command[0] == 'refresh':
      self.refresh()

    elif command[0] == 'help':
      self.help()

  def help(self):
    print "Some help text...."

  def refresh(self):
    self.protocol.send({"action": "refresh"})

  def logout(self):
    pass

  def set_target(self, x, y):
    x = x + self.game.offset[0]
    y = y + self.game.offset[1]
    self.game.player_target = None
    for name,monster in self.game.monsters.items():
      if x in range(monster.spritex - 64, monster.spritex + 64) and y in range(monster.spritey - 64, monster.spritey + 64):
        self.game.player_target = name

  def play(self):

    self.loginManager.delete()
    
    # Send refresh request
    self.protocol.send({"action": "refresh"})

    @self.window.event
    def on_draw():
      self.window.clear()
      self.game.draw()
      self.chatManager.draw()
  
    @self.window.event
    def on_mouse_press(x, y, button, modifiers):
      self.set_target(x,y)
  
    @self.window.event
    def on_key_press(symbol, modifiers):
      if symbol == pyglet.window.key.UP:
        self.protocol.send({"action": "walk", "direction": 'north'})
      if symbol == pyglet.window.key.DOWN:
        self.protocol.send({"action": "walk", "direction": 'south'})
      if symbol == pyglet.window.key.LEFT:
        self.protocol.send({"action": "walk", "direction": 'west'})
      if symbol == pyglet.window.key.RIGHT:
        self.protocol.send({"action": "walk", "direction": 'east'})
      if symbol == pyglet.window.key.SPACE:
        self.protocol.send({"action": "attack", 'target': self.game.player_target})

# For animation testing
#      if symbol == pyglet.window.key.SPACE:
#        self.game.players[self.game.player_name].wait()
#      if symbol == pyglet.window.key.S:
#        self.game.players[self.game.player_name].slash()
#      if symbol == pyglet.window.key.C:
#        self.game.players[self.game.player_name].cast()
#      if symbol == pyglet.window.key.B:
#        self.game.players[self.game.player_name].bow()
#      if symbol == pyglet.window.key.D:
#        self.game.players[self.game.player_name].die()
#      if symbol == pyglet.window.key.T:
#        self.game.players[self.game.player_name].thrust()

  def start(self):
    
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
  
    @self.window.event
    def on_draw():
      self.window.clear()
      self.connectManager.draw()

    @self.window.event
    def on_close():
      reactor.callFromThread(reactor.stop)

      # Return true to ensure that no other handlers
      # on the stack receive the on_close event
      return True
    
    reactor.run(call_interval=1/240.0)
