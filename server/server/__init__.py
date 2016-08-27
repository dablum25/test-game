from twisted.internet import reactor, protocol, endpoints, task
from world.game import Game
from net import GameFactory


def start(source):

  game = Game(source)

  endpoints.serverFromString(reactor, "tcp:10000").listen(GameFactory(game))
  loop = task.LoopingCall(game.loop)
  loop.start(0.01)
  reactor.run()
