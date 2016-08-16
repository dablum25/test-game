import pytmx

class Zone:

  def __init__(self, name, source, title):

    print "Loading zone %s" % name 

    self.name = name
    self.source = source
    self.title  = title
    
    # Logic to load zone file
    self.data = pytmx.TiledMap(source)
    
    self.width = 0
    self.height = 0

    # TODO: Store spawn points as objects in zone?
    

  def open_at(self, x, y):
    '''
    Determine if x,y are open for movement.
    '''
    open_here = True
    for tx,ty,tg in self.data.get_layer_by_name('blocked').iter_data():
      if tx == x and ty == y and tg > 0:
        open_here = False
    return open_here


