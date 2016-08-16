import pyglet
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.constants import ANCHOR_CENTER, HALIGN_LEFT, HALIGN_RIGHT, ANCHOR_RIGHT, ANCHOR_TOP_RIGHT, ANCHOR_BOTTOM_LEFT
from pyglet_gui.gui import Label
from pyglet_gui.text_input import TextInput
from pyglet_gui.theme import Theme
from pyglet_gui.containers import VerticalContainer, HorizontalContainer, Spacer

import os

class ConnectManager(Manager):
  
  def __init__(self, client):

    UI_THEME = Theme({"font": "Lucida Grande",
                 "font_size": 8,
                 "text_color": [255, 255, 255, 255],
                 "gui_color": [255, 0, 0, 255],
                 "input": {
                     "image": {
                         "source": "input.png",
                         "frame": [3, 3, 2, 2],
                         "padding": [3, 3, 2, 3]
                     },
                     # need a focus color
                     "focus_color": [255, 255, 255, 64],
                     "focus": {
                         "image": {
                             "source": "input-highlight.png"
                         }
                     }
                 },
                 "vscrollbar": {
                     "knob": {
                         "image": {
                             "source": "vscrollbar.png",
                             "region": [0, 16, 16, 16],
                             "frame": [0, 6, 16, 4],
                             "padding": [0, 0, 0, 0]
                         },
                         "offset": [0, 0]
                     },
                     "bar": {
                         "image": {
                             "source": "vscrollbar.png",
                             "region": [0, 64, 16, 16]
                         },
                         "padding": [0, 0, 0, 0]
                     }
                 },
                 "button": {
                     "down": {
                         "image": {
                             "source": "button-down.png",
                             "frame": [6, 6, 3, 3],
                             "padding": [12, 12, 4, 2]
                         },
                         "text_color": [0, 0, 0, 255]
                     },
                     "up": {
                         "image": {
                             "source": "button.png",
                             "frame": [6, 6, 3, 3],
                             "padding": [12, 12, 4, 2]
                         }
                     }
                 },
                 "checkbox": {
                     "checked": {
                         "image": {
                             "source": "checkbox-checked.png"
                         }
                     },
                     "unchecked": {
                         "image": {
                             "source": "checkbox.png"
                         }
                     }
                 }
                }, resources_path=os.getcwd() + '/data/theme/')


    self.client = client

    self.connect_button = OneTimeButton(label="Connect", on_release=self.connect)
    self.server_field = TextInput("localhost")
    self.port_field = TextInput("10000")

    Manager.__init__(self, VerticalContainer([self.connect_button, self.server_field, self.port_field]), window=self.client.window,theme=UI_THEME)

  def connect(self, state):
    self.client.try_connect(self.server_field.get_text(),int(self.port_field.get_text()))

class LoginManager(Manager):
  
  def __init__(self, client):
    
    
    UI_THEME = Theme({"font": "Lucida Grande",
                 "font_size": 8,
                 "text_color": [255, 255, 255, 255],
                 "gui_color": [255, 0, 0, 255],
                 "input": {
                     "image": {
                         "source": "input.png",
                         "frame": [3, 3, 2, 2],
                         "padding": [3, 3, 2, 3]
                     },
                     # need a focus color
                     "focus_color": [255, 255, 255, 64],
                     "focus": {
                         "image": {
                             "source": "input-highlight.png"
                         }
                     }
                 },
                 "vscrollbar": {
                     "knob": {
                         "image": {
                             "source": "vscrollbar.png",
                             "region": [0, 16, 16, 16],
                             "frame": [0, 6, 16, 4],
                             "padding": [0, 0, 0, 0]
                         },
                         "offset": [0, 0]
                     },
                     "bar": {
                         "image": {
                             "source": "vscrollbar.png",
                             "region": [0, 64, 16, 16]
                         },
                         "padding": [0, 0, 0, 0]
                     }
                 },
                 "button": {
                     "down": {
                         "image": {
                             "source": "button-down.png",
                             "frame": [6, 6, 3, 3],
                             "padding": [12, 12, 4, 2]
                         },
                         "text_color": [0, 0, 0, 255]
                     },
                     "up": {
                         "image": {
                             "source": "button.png",
                             "frame": [6, 6, 3, 3],
                             "padding": [12, 12, 4, 2]
                         }
                     }
                 },
                 "checkbox": {
                     "checked": {
                         "image": {
                             "source": "checkbox-checked.png"
                         }
                     },
                     "unchecked": {
                         "image": {
                             "source": "checkbox.png"
                         }
                     }
                 }
                }, resources_path=os.getcwd() + '/data/theme/')


    self.client = client
    self.login_button = OneTimeButton(label="Login", on_release=self.login)
    self.username_field = TextInput("username")
    self.password_field = TextInput("password")

    Manager.__init__(self, VerticalContainer([self.login_button, self.username_field, self.password_field]), window=self.client.window,theme=UI_THEME)

  def login(self, state):
    self.client.try_login(self.username_field.get_text(),self.password_field.get_text())



class ChatWindowManager(Manager):
  
  def __init__(self, client):
    
    UI_THEME = Theme({"font": "Lucida Grande",
                 "font_size": 8,
                 "text_color": [255, 255, 255, 255],
                 "gui_color": [255, 0, 0, 255],
                 "input": {
                     "image": {
                         "source": "input.png",
                         "frame": [3, 3, 2, 2],
                         "padding": [3, 3, 2, 3]
                     },
                     # need a focus color
                     "focus_color": [255, 255, 255, 64],
                     "focus": {
                         "image": {
                             "source": "input-highlight.png"
                         }
                     }
                 },
                 "vscrollbar": {
                     "knob": {
                         "image": {
                             "source": "vscrollbar.png",
                             "region": [0, 16, 16, 16],
                             "frame": [0, 6, 16, 4],
                             "padding": [0, 0, 0, 0]
                         },
                         "offset": [0, 0]
                     },
                     "bar": {
                         "image": {
                             "source": "vscrollbar.png",
                             "region": [0, 64, 16, 16]
                         },
                         "padding": [0, 0, 0, 0]
                     }
                 },
                 "button": {
                     "down": {
                         "image": {
                             "source": "button-down.png",
                             "frame": [6, 6, 3, 3],
                             "padding": [12, 12, 4, 2]
                         },
                         "text_color": [0, 0, 0, 255]
                     },
                     "up": {
                         "image": {
                             "source": "button.png",
                             "frame": [6, 6, 3, 3],
                             "padding": [12, 12, 4, 2]
                         }
                     }
                 },
                 "checkbox": {
                     "checked": {
                         "image": {
                             "source": "checkbox-checked.png"
                         }
                     },
                     "unchecked": {
                         "image": {
                             "source": "checkbox.png"
                         }
                     }
                 }
                }, resources_path=os.getcwd() + '/data/theme/')


    self.client = client
    self.message_container = VerticalContainer(content=[], align=HALIGN_LEFT)
    self.messages = Scrollable(height=200, width=360, is_fixed_size=True, content=self.message_container)
    self.text_input = TextInput("", length=20, max_length=256)
    self.send_button = OneTimeButton("Send", on_release=self.submit_message)
    self.enter_field = HorizontalContainer([self.text_input,self.send_button])

    Manager.__init__(self, VerticalContainer([self.messages,self.enter_field]), window=self.client.window, theme=UI_THEME, is_movable=True, anchor=ANCHOR_BOTTOM_LEFT)

  def add_message(self, message):

    self.message_container.add(Label("> " + message[:30] ))
    self.text_input.set_text("")

  def submit_message(self, state):

    message = self.text_input.get_text()
    self.text_input.set_text("")

    if message[0] == "/":
      self.message_container.add(Label("> " + message[:20] ))
      self.client.command(message[1:].split(' '))
    else:
      self.client.chat(message)

