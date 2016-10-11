import pyglet
import time
from animationset import AnimationSet

class Player:

  def __init__(self, title, gender, body, hairstyle, haircolor, armor, head, weapon, x, y):
    
    self.x = x
    self.y = y

    self.action    = 'wait'
    self.direction = 'south'
    self.armor     = armor
    self.gender    = gender
    self.body      = body
    self.hairstyle = hairstyle
    self.haircolor = haircolor
    self.head      = head
    self.weapon    = weapon
   
    # Movement
    self.destx = self.x
    self.desty = self.y
    self.spritex = self.x * 32
    self.spritey = self.y * 32
    self.speed = 4

    self.animation = AnimationSet(self.gender, self.body, self.hairstyle, self.haircolor, self.armor, self.head, self.weapon)
    
    self.title = title
    self.label = pyglet.text.Label(self.title,
                                   font_name='Times New Roman',
                                   font_size=12,
                                   color=(0,0,255,255),
                                   width=32,
                                   x=self.spritex,
                                   y=self.spritey)

    # Scheduel our update frequency
    pyglet.clock.schedule_interval(self.update, 1/240.0)

  def set_weapon(self,weapon):

    self.weapon = weapon
    self.animation = AnimationSet(self.gender, self.body, self.hairstyle, self.haircolor, self.armor, self.head, self.weapon)

  def set_armor(self,armor):
    
    self.armor = armor
    self.animation = AnimationSet(self.gender, self.body, self.hairstyle, self.haircolor, self.armor, self.head, self.weapon)

  def set_head(self,head):
    
    self.head = head
    self.animation = AnimationSet(self.gender, self.body, self.hairstyle, self.haircolor, self.armor, self.head, self.weapon)

  def wait(self, dt=0):
    self.action = 'wait'

  def go(self, direction, start, end):

    self.wait()
  
    self.x = start[0]
    self.y = start[1]
    self.spritex = start[0] * 32
    self.spritey = start[1] * 32
    self.destx = end[0]
    self.desty = end[1]
    self.direction = direction

  def slash(self):
    
    if self.action == 'wait':
      self.action = 'slash'
      pyglet.clock.schedule_once(self.wait,1.5)

  def thrust(self):
    
    if self.action == 'wait':
      self.action = 'thrust'
      pyglet.clock.schedule_once(self.wait,1.5)
  
  def bow(self):
    
    if self.action == 'wait':
      self.action = 'bow'
      pyglet.clock.schedule_once(self.wait,1.5)

  def cast(self):
    
    if self.action == 'wait':
      self.action = 'cast'
      pyglet.clock.schedule_once(self.wait,1.5)

  def die(self):
    
    self.wait()
    self.action = 'die'

  def update(self, dt):
    # Don't move if we are doing something else
    if self.action in [ 'slash', 'die', 'cast', 'thrust', 'die', 'bow' ]:
      return

    if self.direction == 'north':
      if self.spritey < self.desty * 32:
        self.spritey += self.speed
        self.action = 'walk'
      else:
        self.y = self.desty
        self.spritey = self.desty * 32
        self.action = 'wait'

    elif self.direction == 'south':
      if self.spritey > self.desty * 32:
        self.spritey -= self.speed
        self.action = 'walk'
      else:
        self.y = self.desty
        self.spritey = self.desty * 32
        self.action = 'wait'
    
    elif self.direction == 'east':
      if self.spritex < self.destx * 32:
        self.spritex += self.speed
        self.action = 'walk'
      else:
        self.x = self.destx
        self.spritex = self.destx * 32
        self.action = 'wait'
    
    elif self.direction == 'west':
      if self.spritex > self.destx * 32:
        self.spritex -= self.speed
        self.action = 'walk'
      else:
        self.x = self.destx
        self.spritex = self.destx * 32
        self.action = 'wait'
     
  def draw(self, offset, target):
    self.animation.draw(self.action, self.direction, self.spritex, self.spritey, offset)
    self.label.x = self.spritex - offset[0]
    self.label.y = self.spritey - offset[1] + 64
    if target:
      self.label.bold = True
      self.label.font_size = 14
    else:
      self.label.bold = False
      self.label.font_size = 12
    self.label.draw()
