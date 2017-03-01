import ConfigParser

def load_quests(world):

  config = ConfigParser.RawConfigParser()
  config.read('data/quests.ini')
  
  
  for name in config.sections():
    title = config.get(name,'title')
    dialog = config.get(name,'dialog')
    
    world.quests[name] = Quest(name, title, dialog, world)  

  

class Quest:
  '''
  Generates PlayerQuest objects. Held by Npc.
  '''
  def __init__(self, name, title, dialog, world):

    self.name   = name
    self.title  = title
    self.dialog = dialog
    self.world  = world


    print "Loaded QUEST %s" % self.name
