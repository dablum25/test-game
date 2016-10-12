from item import Item
import copy

class ShopItem:
  '''
  Spawns items in merchant inventory
  '''
  mi_index = 0

  def __init__(self, title, gear_type, slot, hit, dam, arm, value, icon):

    self.title = title
    self.gear_type = gear_type
    self.slot = slot
    self.hit = hit
    self.dam = dam
    self.arm = arm
    self.value = value 
    self.icon = icon

  def create(self, buyer_name, world):
    
    name = "%s-%s" % ( self.gear_type, self.mi_index )
    self.mi_index += 1
    
    bh = { 'name': name, 
           'title': self.title, 
           'gear_type': self.gear_type, 
           'player': buyer_name, 
           'slot': self.slot,
           'container': None,
           'hit': self.hit, 
           'dam': self.dam, 
           'arm': self.arm,
           'icon': self.icon,
           'equipped': False }
    world.items[name] = Item(**copy.deepcopy(bh))

class Shop:

  def __init__(self, name, title, itemset, world):

    self.title = title
    self.name = name
    self.world = world
    self.inventory = {}

    self.message = "Welcome to my shop! What would you like to buy?"

    if itemset == 'armorer':
      self.armorer()
    elif itemset == 'outfitter':
      self.outfitter()
    elif itemset == 'magic':
      self.magic()

  def armorer(self):
    '''
    Advanced weapons and armor
    '''
    self.inventory['sword']  = ShopItem('Sword','sword','weapon',3,3,0,10,'sword')
    self.inventory['bow']  = ShopItem('Small Bow','bow','weapon',2,3,0,10,'bow')
    self.inventory['chain_armor']  = ShopItem('Chain','chain','armor',0,0,4,10,'chain_armor')

  def outfitter(self):
    '''
    Basic gear
    '''
    self.inventory['sword']  = ShopItem('Sword','sword','weapon',3,3,0,10,'sword')
    self.inventory['bow']  = ShopItem('Small Bow','bow','weapon',2,3,0,10,'bow')
    self.inventory['hood']   = ShopItem('Hood','clothhood','head',0,0,1,10,'cloth_hood')
    self.inventory['wand']   = ShopItem('Wooden Wand','wand','weapon',1,0,0,10,'wand')

  def magic(self):
    '''
    Magical weapons and equipment
    '''
    self.inventory['hood']   = ShopItem('Hood','clothhood','head',0,0,1,10,'cloth_hood')
    self.inventory['wand']   = ShopItem('Wooden Wand','wand','weapon',1,0,0,10,'wand')

  def get_inventory(self):

    inv = {}
    for name,item in self.inventory.items():
      inv[name] = { 'title': item.title, 'slot': item.slot, 'hit': item.hit, 'dam': item.dam, 'arm': item.arm, 'value': item.value, 'icon': item.icon }

    return inv

  def sell(self, item_name, seller_name):
    
    # remove sold object from game world
    del self.world.items[item_name]

    # TODO: pay player for item

  def buy(self, item_name, buyer_name):
    
    # Add purchased item to game world
    self.inventory[item_name].create(buyer_name, self.world)

    # TODO: deduct gold from player for purchase
