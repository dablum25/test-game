import ConfigParser

def load_quests(world):

  config = ConfigParser.RawConfigParser()
  config.read('data/quests.ini')
  
  
  for name in config.sections():
    title = config.get(name,'title')
    dialog = config.get(name,'dialog')
    level = config.getint(name,'level')
    item_reward = config.get(name,'item_reward')
    exp_reward = config.getint(name,'exp_reward')
    gold_reward = config.getint(name,'gold_reward')
    requires = config.get(name,'requires')

    
    world.quests[name] = Quest(name, title, dialog, world, level, item_reward, exp_reward, gold_reward, requires)  
  

class Quest:
  '''
  Generates PlayerQuest objects. Held by Npc.
  '''
  def __init__(self, name, title, dialog, world, level, item_reward, exp_reward, gold_reward, requires):

    self.name        = name
    self.title       = title
    self.dialog      = dialog
    self.world       = world
    self.level       = level
    self.item_reward = item_reward
    self.exp_reward  = exp_reward
    self.gold_reward = gold_reward
    self.requires    = requires

    print "Loaded QUEST %s" % self.name

  def assign(self, player_name):

    if self.avaliable_to(player_name):

      self.world.players[player_name].quests[self.name] = PlayerQuest(self.name,self.world)
    
      return { 'type': 'message', 'message': "You accept the quest." }
    
    else:
      return { 'type': 'message', 'message': "That quest is not avaliable." }

  def avaliable_to(self, player_name):
    
    # dont already have quest
    if self.world.players[player_name].quests.has_key(self.name):
      print "already have"
      return False 

    # player is appropriate level
    if self.world.players[player_name].level < self.level:
      print "wrong level"
      return False

    # player has completed prereqs
    if self.requires:
      if not self.world.players[player_name].quests.has_key(self.requires):
        print "don't have prereq"
        return False

      if not self.world.players[player_name].quests[self.requires].is_complete:
        print "dont have prereq complete"
        return False

    return True


class PlayerQuest:
  '''
  Track player quest progression.
  '''

  def __init__(self, name, world):

    self.name  = name
    self.world = world

  
  def is_complete(self):
    # Test if all goals are met
    return False
    
  def get_log_entry(self):
  
    title = self.world.quests[self.name].title
    dialog = self.world.quests[self.name].dialog
    
    return { 'title': title, 'dialog': dialog } 
