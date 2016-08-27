import time

class Monster:

  def __init__(self, source, name, title, x, y, zone, hp, mp, hit, dam, arm):
    
    self.source = source
    self.title = title
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone
    self.free_at = time.time() # next time monster will be free to perform another action
    self.spawn = None
    self.target = None
    self.fighting = False
    
    self.hp = hp
    self.mp = mp
    self.hit = hit
    self.dam = dam
    self.arm = arm


  def reset(self):
    
    self.free_at = time.time() + 2.0

  def state(self):

    return { 'title': self.title, 'source': self.source, 'name': self.name, 'x': self.x, 'y': self.y, 'zone': self.zone, }

  def free(self):

    if time.time() - self.free_at > 2.0:
      return True
    else:
      return False
