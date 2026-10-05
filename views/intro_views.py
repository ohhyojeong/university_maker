from .system_views import SystemViews

class IntroViews(SystemViews):
  def __init__(self):
    pass

  @staticmethod
  def introTitle():
    SystemViews.headline('대학생 시뮬레이터')

  @staticmethod
  def introMenu() -> int:
    menus = '새로하기', '이어하기', '종료'
    SystemViews.menu(*menus)
    SystemViews.lineBreak(True)

    return SystemViews.choice('메뉴 선택', len(menus))