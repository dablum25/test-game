import time

class Player:

  def __init__(self, title, source, name, password, x, y, zone, spells, hp, mp, hit, dam, arm):

    print "Loading player %s" % name

    self.title = title
    self.source = source
    self.name = name
    self.x = x
    self.y = y
    self.zone = zone
    self.online = False
    self.password = password
    self.free_at = time.time() # next time player will be free to perform another action
    self.stats = { 'xp': 0, 'hp': [hp,hp], 'mp': [mp,mp], 'hit': hit, 'dam': dam, 'arm': arm }
    self.target = None
    self.fighting = False
    self.spells = spells # list of spells known by this player

  def state(self):

    return { 'title': self.title, 'name': self.name, 'source': self.source, 'x': self.x, 'y': self.y, 'zone': self.zone, }

  def free(self):

    if time.time() - self.free_at > 1.0:
      return True
    else:
      return False
