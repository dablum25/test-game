import time

class Player:

  def __init__(self, title, source, name, password, x, y, zone, spells, hp, mp, hit, dam, arm):

    self.title = title
    self.source = source
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone
    self.online = False
    self.password = password
    self.free_at = time.time() # next time player will be free to perform another action
    self.target = None
    self.fighting = False
    self.spells = spells # list of spells known by this player

    self.hp = [ hp, hp ]
    self.mp = [ mp, mp ]
    self.hit = hit
    self.dam = dam
    self.arm = arm

  def state(self):

    return { 'title': self.title, 'name': self.name, 'source': self.source, 'x': self.x, 'y': self.y, 'zone': self.zone, }

  def reset(self):
    
    self.free_at = time.time() + 0.75

  def free(self):

    if time.time() - self.free_at > 0.75:
      return True
    else:
      return False
