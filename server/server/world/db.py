import sqlite3

class Db:

  def __init__(self, source):

    self.source = source
    self.conn = sqlite3.connect(source)

  def load_zones(self):
    pass

  def load_monsters(self):
    pass

  def load_spawns(self):
    pass

  def load_containers(self):
    pass

  def load_items(self):
    pass

  def save_item(self):
    pass

  def load_spells(self):
    pass

  def load_players(self):

    cursor = self.conn.cursor()

    cursor.execute('SELECT * FROM players')
    
    players = []
    for player in cursor.fetchall():
      
      players.append({ 'name': player[0],
                       'title': player[1],
                       'x': player[2],
                       'y': player[3],
                       'zone': player[4],
                       'password': player[5],
                       'spells': player[6].split(','),
                       'hit': player[7],
                       'arm': player[8],
                       'dam': player[8],
                       'hp': player[8],
                       'mp': player[8],})

    return players

  def save_player(self, name):

    pass


if __name__ == '__main__':

  db = Db('data/gloomsum.db')

  print db.load_players()
