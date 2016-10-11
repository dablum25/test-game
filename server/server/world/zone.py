import pytmx
import time
from astar import *

class Zone:
  '''
  Zone with astar pathfinding.
  '''

  def __init__(self, name, source, title):

    self.name = name
    self.source = source
    self.title  = title
    
    # Logic to load zone file
    self.data = pytmx.TiledMap(source)
    
    self.width = self.data.width
    self.height = self.data.height

    self.blocked = self.data.layers.index(self.data.get_layer_by_name('blocked'))
 
    self.graph = GridWithWeights(self.width, self.height)
   
    self.graph.walls = [ (x,self.height - y - 1) for x,y,gid in self.data.layers[self.blocked].tiles() ] 
  
  def heuristic(self, a,b):
    (x1,y1) = a
    (x2,y2) = b

    return abs(x1 - x2) + abs(y1 - y2)

  def get_path(self, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    if start == goal:
      return []

    if goal[0] > self.width:
      return []
    
    if goal[0] < 0:
      return []
      
    if goal[1] > self.height:
      return []
    
    if goal[1] < 0:
      return [] 

    if goal in self.graph.walls:
      return []
  
    while not frontier.empty():
      current = frontier.get()
  
      if current == goal:
        break
  
      for next in self.graph.neighbors(current):
        new_cost = cost_so_far[current] + self.graph.cost(current, next)
        if next not in cost_so_far or new_cost < cost_so_far[next]:
          cost_so_far[next] = new_cost
          priority = new_cost + self.heuristic(goal, next)
          frontier.put(next, priority)
          came_from[next] = current
  
    path = [ current ]
    while current != start:
      current = came_from[current]
      path.append(current)
    
    path.reverse()
    path.pop(0)
    return path
 
  def open_at(self, x, y):
    '''
    Determine if x,y are open for movement.
    '''
    if x > self.width - 1:
      return False
    elif x < 0:
      return False
    elif y > self.height - 1:
      return False
    elif y < 0:
      return False
    elif self.data.get_tile_gid(x, self.height - y - 1, self.blocked) > 0:
      return False
    else:
      return True

class ZoneWithObjects:
  '''
  Zone with astar pathfinding.
  '''

  def __init__(self, name, source, title, world):

    self.name = name
    self.source = source
    self.title  = title
    self.world = world
    
    # Logic to load zone file
    self.data = pytmx.TiledMap(source)
    
    self.width = self.data.width
    self.height = self.data.height

    self.blocked = self.data.layers.index(self.data.get_layer_by_name('blocked'))
 
    self.graph = GridWithWeights(self.width, self.height)
   
    self.graph.walls = [ (x,self.height - y - 1) for x,y,gid in self.data.layers[self.blocked].tiles() ] 
 
 
    # Load npc spawns, monster spawns, and warps
    self.npc_spawn_layer     = self.data.layers.index(self.data.get_layer_by_name('npc_spawns'))
    self.monster_spawn_layer = self.data.layers.index(self.data.get_layer_by_name('monster_spawns'))
    self.warp_layer          = self.data.layers.index(self.data.get_layer_by_name('warps'))

    self.meta_layer = self.data.layers.index(self.data.get_layer_by_name('meta'))
    
    for obj in self.meta_layer:
      print obj
         
  def heuristic(self, a,b):
    (x1,y1) = a
    (x2,y2) = b

    return abs(x1 - x2) + abs(y1 - y2)

  def get_path(self, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    if start == goal:
      return []

    if goal[0] > self.width:
      return []
    
    if goal[0] < 0:
      return []
      
    if goal[1] > self.height:
      return []
    
    if goal[1] < 0:
      return [] 

    if goal in self.graph.walls:
      return []
  
    while not frontier.empty():
      current = frontier.get()
  
      if current == goal:
        break
  
      for next in self.graph.neighbors(current):
        new_cost = cost_so_far[current] + self.graph.cost(current, next)
        if next not in cost_so_far or new_cost < cost_so_far[next]:
          cost_so_far[next] = new_cost
          priority = new_cost + self.heuristic(goal, next)
          frontier.put(next, priority)
          came_from[next] = current
  
    path = [ current ]
    while current != start:
      current = came_from[current]
      path.append(current)
    
    path.reverse()
    path.pop(0)
    return path
 
  def open_at(self, x, y):
    '''
    Determine if x,y are open for movement.
    '''
    if x > self.width - 1:
      return False
    elif x < 0:
      return False
    elif y > self.height - 1:
      return False
    elif y < 0:
      return False
    elif self.data.get_tile_gid(x, self.height - y - 1, self.blocked) > 0:
      return False
    else:
      return True

