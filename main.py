import os
from managers import DataManager
from controllers import SceneController

class main:
  def __init__(self):
    basePath = os.path.dirname(__file__)
    store = DataManager(basePath=basePath)

    self.scene = SceneController(store)
    self.scene.intro()


if __name__ == '__main__':
  main()