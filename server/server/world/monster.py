import time

class Monster:

  def __init__(self, source, name, title, x, y, zone):
    
    self.source = source
    self.title = title
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone
    self.free_at = time.time() # next time monster will be free to perform another action
    self.spawn = None
    self.stats = { 'hp': [5,5], 'mp': [0,0], 'hit': 1, 'dam': 0, 'arm': 1 }
    self.target = None
    self.fighting = False
    # TODO: Monster item drops on death

  def state(self):

    return { 'title': self.title, 'source': self.source, 'name': self.name, 'x': self.x, 'y': self.y, 'zone': self.zone, }

  def free(self):

    if time.time() - self.free_at > 1.0:
      return True
    else:
      return False
