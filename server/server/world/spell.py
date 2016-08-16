class Spell:

  def __init__(self, name, title):
    
    print "Loading container %s" % name

    self.title = title
    self.name = name

  def state(self):

    return { 'title': self.title, 'name': self.name }

