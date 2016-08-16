import pyglet

class Character:

  def __init__(self, title, source, x, y):
    
    self.x = x
    self.y = y

    raw = pyglet.image.load(source)
    grid = pyglet.image.ImageGrid(raw, 21, 13)
    self.action = 'wait'
    self.direction = 'south'
   
    self.title = title

    # Movement
    self.destx = self.x
    self.desty = self.y
    self.spritex = self.x * 32
    self.spritey = self.y * 32

    # Frames within grid (e,s,w,n)
    # die 0:5, 0:5, 0:5, 0:5
    # bow 13:25, 26:38, 39:51, 52:64
    # slash 65:73:, 78:86, 91:99, 104:112
    # wait 117:117, 130:130, 143:143, 156:156
    # walk 118:126, 131:139, 144:152, 157:165
    # thrust 169:177, 182:190, 195:203, 208:213
    # cast 221:228, 234:42, 247:255, 260:268

    self.sprites = {}
    for a in [ 'die', 'bow', 'slash', 'wait', 'walk', 'thrust', 'cast' ]:
      self.sprites[a] = {}
      for d in [ 'east', 'south', 'west', 'north' ]:
        self.sprites[a][d] = []

    self.sprites['die']['east'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[0:6], 0.15, False))
    self.sprites['die']['south'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[0:6], 0.15, False))
    self.sprites['die']['west'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[0:6], 0.15, False))
    self.sprites['die']['north'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[0:6], 0.15, False))

    self.sprites['bow']['east'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[13:26], 0.077, True))
    self.sprites['bow']['south'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[26:39], 0.077, True))
    self.sprites['bow']['west'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[39:52], 0.077, True))
    self.sprites['bow']['north'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[52:65], 0.077, True))

    self.sprites['slash']['east'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[65:71], 0.125, True))
    self.sprites['slash']['south'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[78:84], 0.125, True))
    self.sprites['slash']['west'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[91:97], 0.125, True))
    self.sprites['slash']['north'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[104:110], 0.125, True))

    self.sprites['wait']['east'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[117:118], 1, True))
    self.sprites['wait']['south'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[130:131], 1, True))
    self.sprites['wait']['west'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[143:144], 1, True))
    self.sprites['wait']['north'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[156:157], 1, True))

    self.sprites['walk']['east'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[118:126], 0.125, True))
    self.sprites['walk']['south'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[131:139], 0.125, True))
    self.sprites['walk']['west'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[144:152], 0.125, True))
    self.sprites['walk']['north'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[157:165], 0.125, True))

    self.sprites['thrust']['east'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[169:177], 0.166, True))
    self.sprites['thrust']['south'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[182:190], 0.166, True))
    self.sprites['thrust']['west'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[195:203], 0.166, True))
    self.sprites['thrust']['north'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[208:216], 0.166, True))
    
    self.sprites['cast']['east'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[223:228], 0.177, True))
    self.sprites['cast']['south'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[236:241], 0.177, True))
    self.sprites['cast']['west'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[248:253], 0.177, True))
    self.sprites['cast']['north'] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(grid[261:266], 0.177, True))

    # Scheduel our update frequency
    pyglet.clock.schedule_interval(self.update, 1/240.0)

  def wait(self):
    self.action = 'wait'

  def go(self, direction, start):

    self.wait()
  
    self.x = start[0]
    self.y = start[1]
    self.destx = start[0]
    self.desty = start[1]

    if direction == 'north':
      self.desty += 1
      self.direction = 'north'
    elif direction == 'south':
      self.desty -= 1
      self.direction = 'south'
    elif direction == 'east':
      self.destx += 1
      self.direction = 'east'
    elif direction == 'west':
      self.destx -= 1
      self.direction = 'west'

  def slash(self):
    
    if self.action == 'wait':
      self.action = 'slash'

  def thrust(self):
    
    if self.action == 'wait':
      self.action = 'thrust'
  
  def bow(self):
    
    if self.action == 'wait':
      self.action = 'bow'

  def cast(self):
    
    if self.action == 'wait':
      self.action = 'cast'

  def die(self):

    if self.action == 'wait':
      self.action = 'die'

  def update(self, dt):
    
    # Don't move if we are doing something else
    if self.action in [ 'slash', 'die', 'cast', 'thrust', 'die', 'bow' ]:
      return
    
    if self.direction == 'north':
      if self.spritey < self.desty * 32:
        self.spritey += 1
        self.action = 'walk'
      else:
        self.y = self.desty
        self.spritey = self.desty * 32
        self.action = 'wait'

    elif self.direction == 'south':
      if self.spritey > self.desty * 32:
        self.spritey -= 1
        self.action = 'walk'
      else:
        self.y = self.desty
        self.spritey = self.desty * 32
        self.action = 'wait'
    
    elif self.direction == 'east':
      if self.spritex < self.destx * 32:
        self.spritex += 1
        self.action = 'walk'
      else:
        self.x = self.destx
        self.spritex = self.destx * 32
        self.action = 'wait'
    
    elif self.direction == 'west':
      if self.spritex > self.destx * 32:
        self.spritex -= 1
        self.action = 'walk'
      else:
        self.x = self.destx
        self.spritex = self.destx * 32
        self.action = 'wait'
     
  def draw(self, offset):
    offset_x = offset[0]
    offset_y = offset[1]
    self.sprites[self.action][self.direction].set_position(self.spritex - 16 - offset_x, self.spritey - offset_y)
    self.sprites[self.action][self.direction].draw()

