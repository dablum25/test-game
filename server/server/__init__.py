from twisted.internet import reactor, protocol, endpoints, task
from world.game import Game
from net import GameFactory


def start():

  game = Game()

  game.load_players()
  game.load_zones()
  game.load_spawns()
  game.load_items()
  game.load_spells()
  game.load_containers()
 
  endpoints.serverFromString(reactor, "tcp:10000").listen(GameFactory(game))
  loop = task.LoopingCall(game.loop)
  loop.start(0.01)
  reactor.run()
