class Item:

  def __init__(self, source, name, title, player, slot, container, hit, dam, arm, equipped):

    self.title = title
    self.source = source
    self.name = name
    self.player = player
    self.equipped = equipped
    self.container = container
    self.slot = slot # 'head', 'weapon', 'body', 'feet' or None
    self.stats = { 'weight': 0, 'dam': dam, 'hit': hit, 'arm': arm }

  def state(self):
    
    return { 'title': self.title, 'name': self.name, 'source': self.source, 'player': self.player, 'slot': self.slot, 'equipped': self.equipped, 'stats': self.stats }

