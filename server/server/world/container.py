class Container:

  def __init__(self, title, name, x, y, zone):
    
    self.title = title
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone

  def state(self):

    return { 'title': self.title, 'name': self.name, 'x': self.x, 'y': self.y, 'zone': self.zone }

