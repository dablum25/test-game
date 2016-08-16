#!/usr/bin/python

import sys

sys.path.append('deps')

from client import Client

def run():

  client = Client()
  client.start() 
