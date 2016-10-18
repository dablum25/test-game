class Item:

  def __init__(self, name, title, gear_type, player, slot, container, hit, dam, arm, equipped, icon, value):

    self.title = title
    self.name = name
    self.player = player
    self.equipped = equipped
    self.container = container
    self.gear_type = gear_type # 'none', 'leather', 'chain', 'plate', 'hat', 'clothhood', 'chainhood', 'chainhat', 'helm', 'sword', 'spear', 'wand', 'bow'
    self.slot = slot # 'head', 'weapon', 'armor', or 'none'
    self.hit = hit
    self.dam = dam
    self.arm = arm
    self.icon = icon
    self.value = value

    print "Loaded ITEM",self.state()

  def state(self):
    
    return { 'title': self.title, 'name': self.name, 'slot': self.slot, 'equipped': self.equipped, 'gear_type': self.gear_type, 'icon': self.icon, 'hit': self.hit, 'dam': self.dam, 'arm': self.arm, 'value': self.value }

