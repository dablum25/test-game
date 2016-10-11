class Quest:
  '''
  Generates PlayerQuest objects. Held by Npc.
  '''
  def __init__(self, name, title, dialog, world):

    self.name   = name
    self.title  = title
    self.dialog = dialog
    self.world  = world
    

