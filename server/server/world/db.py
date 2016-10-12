import sqlite3

class Db:

  def __init__(self, source):

    self.source = source
    self.conn = sqlite3.connect(source)

  def load_zones(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM zones')
    
    zones = []
    for zone in cursor.fetchall():
      
      zones.append({ 'name': zone[0],
                     'source': zone[1],
                     'title': zone[2],})

    return zones

  def load_warps(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM warps')
    
    zones = []
    for zone in cursor.fetchall():
      
      zones.append({ 'start_zone': zone[0],
                     'start_x': zone[1],
                     'start_y': zone[2],
                     'end_zone': zone[3],
                     'end_x': zone[4],
                     'end_y': zone[5],})

    return zones


  def load_monster_spawns(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM monster_spawns')
    
    spawns = []
    for spawn in cursor.fetchall():
      
      spawns.append({ 'name': spawn[0],
                      'title': spawn[1],
                      'source': spawn[2],
                      'zone': spawn[3],
                      'x': spawn[4],
                      'y': spawn[5],
                      'spawn_max': spawn[6],
                      'hp': spawn[7],
                      'mp': spawn[8],
                      'hit': spawn[9],
                      'dam': spawn[10],
                      'arm': spawn[11],})

    return spawns

  def load_npc_spawns(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM npc_spawns')
    
    spawns = []
    for spawn in cursor.fetchall():
      
      spawns.append({ 'name': spawn[0],
                      'title': spawn[1],
                      'gender': spawn[2],
                      'body': spawn[3], 
                      'hairstyle': spawn[4],
                      'haircolor': spawn[5],
                      'armor': spawn[6],
                      'head': spawn[7],
                      'weapon': spawn[8],
                      'zone': spawn[9],
                      'x': spawn[10],
                      'y': spawn[11],
                      'spawn_max': spawn[12],
                      'hp': spawn[13],
                      'mp': spawn[14],
                      'hit': spawn[15],
                      'dam': spawn[16],
                      'arm': spawn[17],
                      'shop': spawn[18],
                      'quest': spawn[19],
                      'villan': bool(spawn[20]),})

    return spawns

  def load_shops(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM shops')
    
    shops = []
    for shop in cursor.fetchall():
      
      shops.append({ 'name': shop[0],
                     'title': shop[1],
                     'itemset': shop[2],})

    return shops
  
  def load_quests(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM quests')
    
    quests = []
    for quest in cursor.fetchall():
      
      quests.append({ 'name': quest[0],
                      'title': quest[1],
                      'dialog': quest[2],})

    return quests

  def load_items(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM items')
    
    items = []
    for item in cursor.fetchall():
      
      items.append({ 'name': item[0],
                     'title': item[1],
                     'gear_type': item[2],
                     'slot': item[3],
                     'player': item[4],
                     'container': item[5],
                     'dam': item[6],
                     'hit': item[7],
                     'arm': item[8],
                     'equipped': bool(item[9]),
                     'icon': item[10],
                     'value': item[11],})

    return items

  def save_item(self):
    pass

  def load_spells(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM spells')
    
    spells = []
    for spell in cursor.fetchall():
      spells.append({ 'name': spell[0],
                      'title': spell[1],
                      'level': spell[2],
                      'caster_source': spell[3],
                      'target_source': spell[4],
                      'range': spell[5],
                      'target_hp': spell[6],
                      'target_mp': spell[7],
                      'target_hit': spell[8],
                      'target_dam': spell[9],
                      'target_arm': spell[10],
                      'caster_hp': spell[11],
                      'caster_mp': spell[12],
                      'caster_hit': spell[13],
                      'caster_dam': spell[14],
                      'caster_arm': spell[15],
                      'description': spell[16],
                      'mana_cost': spell[17],})

    return spells

  def load_players(self):

    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM players')
    
    players = []
    for player in cursor.fetchall():
      
      players.append({ 'name': player[0],
                       'title': player[1],
                       'gender': player[2],
                       'body': player[3],
                       'hairstyle': player[4],
                       'haircolor': player[5],
                       'zone': player[6],
                       'x': player[7],
                       'y': player[8],
                       'password': player[9],
                       'spells': player[10].split(','),
                       'hit': player[11],
                       'arm': player[12],
                       'dam': player[13],
                       'hp': player[14],
                       'mp': player[15],})

    return players

  def save_player(self, name):

    pass


if __name__ == '__main__':

  db = Db('gloomsum.db')

  print db.load_players()
  print db.load_spells()
  print db.load_zones()
  print db.load_spawns()
  print db.load_items()
  print db.load_warps()

