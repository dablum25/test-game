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

  def load_spawns(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM spawns')
    
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

  def load_containers(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM containers')
    
    containers = []
    for container in cursor.fetchall():
      
      containers.append({ 'name': container[0],
                          'title': container[1],
                          'x': container[2],
                          'y': container[3],
                          'zone': container[4],
                          'source_open': container[5],
                          'source_closed': container[6],})

    return containers

  def load_items(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM items')
    
    items = []
    for item in cursor.fetchall():
      
      items.append({ 'name': item[0],
                     'title': item[1],
                     'source': item[2],
                     'slot': item[3],
                     'player': item[4],
                     'container': item[5],
                     'dam': item[6],
                     'hit': item[7],
                     'arm': item[8],
                     'equipped': bool(item[9]),})

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
                      'description': spells[16],})

    return spells

  def load_warps(self):
    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM warps')
    
    warps = []
    for warp in cursor.fetchall():
      
      warps.append({ 'name': warp[0],
                     'start_zone': warp[1],
                     'end_zone': warp[2],
                     'start_x': warp[2],
                     'start_y': warp[2],
                     'end_x': warp[2],
                     'end_y': warp[2],})

    return warps


  def load_players(self):

    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM players')
    
    players = []
    for player in cursor.fetchall():
      
      players.append({ 'name': player[0],
                       'title': player[1],
                       'source': player[2],
                       'zone': player[3],
                       'x': player[4],
                       'y': player[5],
                       'password': player[6],
                       'spells': player[7].split(','),
                       'hit': player[8],
                       'arm': player[9],
                       'dam': player[10],
                       'hp': player[11],
                       'mp': player[12],})

    return players

  def save_player(self, name):

    pass


if __name__ == '__main__':

  db = Db('data/gloomsum.db')

  print db.load_players()
  print db.load_spells()
  print db.load_zones()
  print db.load_spawns()
  print db.load_items()
  print db.load_containers()
  print db.load_warps()

