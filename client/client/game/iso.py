# Support for isometric zones and characters
#
import copy
import pyglet
import xml.etree.ElementTree as ET

class AnimationSet:

  def __init__(self, source):
    
    tree = ET.parse(source)
    root = tree.getroot()

    self.data = {}

    self.img_path = root.attrib['path']
    
    raw = pyglet.image.load(root.attrib['path'])
    
    grid_width = int(root.attrib['img_width']) / int(root.attrib['frame_width'])
    grid_height = int(root.attrib['img_height']) / int(root.attrib['frame_height'])
    
    grid = pyglet.image.ImageGrid(raw, grid_width, grid_height)
    
    for direction in root:
      self.data[direction.attrib['name']] = {}
      for action in direction:
        
        first = int(action.attrib['first'])
        last  = int(action.attrib['last'])
        
        speed = 0.15
        loop  = True
        
        animation = pyglet.image.Animation.from_image_sequence(grid[first:last], speed, loop)
        
        self.data[direction.attrib['name']][action.attrib['name']] = animation

  def __getitem__(self, direction):
    
    return self.data[direction]

  
class Character:

  def __init__(self, x, y, body_animation):
  
    self.x = x
    self.y = y

    self.draw_x = 
    self.draw_y =

    self._body = copy(body)
    self._weapon = None
    self._sheild = None

    self.action = 'action'
    self.direction = 'south'

  def set_body(self, body):
    
    self._body = copy(body)

  def set_weapon(self, weapon):

    self._weapon = copy(weapon)

  def set_shield(self, shield):
    
    self._shield = copy(shield)

  def draw(self, offset):

    if self._body:
      self._body[self._action][self._direction].draw(offset)
    if self._weapon:
      self._weapon[self._action][self._direction].draw(offset)
    if self._shield:
      self._shield[self._action][self._direction].draw(offset)

    



if __name__ == '__main__':

  anim = AnimationSet('data/flare_resources/animationsets/male_clothes.xml')


