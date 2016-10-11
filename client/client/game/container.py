import pyglet

class Container:

  def __init__(self, title, x, y, source, source_width=32, source_height=32, source_x=0, source_y=0):
   
    self.title = title
    self.x     = x
    self.y     = y

    raw = pyglet.image.load(source)
    self.sprite = pyglet.sprite.Sprite(raw.get_region(source_x,source_y,source_width,source_height), self.x * 32, self.y * 32)
    
  def draw(self, offset, target):
    offset_x = offset[0]
    offset_y = offset[1]
    self.sprite.set_position(self.x * 32 - offset_x, self.y * 32 - offset_y)
    if target:
      self.sprite.color = (255,0,0)
    else:
      self.sprite.color = (255,255,255)

    self.sprite.draw()
