import pyglet

class Container:

  def __init__(self, name, title, x, y, source, source_width=32, source_height=32, source_x=0, source_y=0):
   
    self.name  = name
    self.title = title
    self.x     = x
    self.y     = y

    raw = pyglet.image.load(source)
    self.image = py
    
  def draw(self, offset):
    pass
