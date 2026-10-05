from utils import padByDisplayWidth

class SystemViews:

  @staticmethod
  def lineBreak(bold=False):
    print(f"{(bold and '=' or '-')*50}")

  @staticmethod
  def headline(*contents):
    SystemViews.lineBreak(True)
    print()
    for content in contents:
      print(padByDisplayWidth(content, 50, align='center'))
    print()
    SystemViews.lineBreak(True)

  @staticmethod
  def subtitle(*contents):
    SystemViews.lineBreak()
    for content in contents:
      print(padByDisplayWidth(content, 50, align='center'))
    SystemViews.lineBreak()

  @staticmethod
  def menu(*menus):
    for index, menu in enumerate(menus):
      print(f'  [{index + 1}] {menu}')

  @staticmethod
  def input(placeholder):
    value = input(f'{placeholder} >>> ').strip()
    print()
    return value

  @staticmethod
  def choice(placeholder, max, min = 1):
    while True:
      value = SystemViews.input(placeholder)
      if value is None:
        continue
      else:
        try:
          value = int(value)
          if min > value or value > max:
            SystemViews.errorMessage(f'{min}-{max}사이의 숫자를 입력해 주세요')
            continue
          else:
            return value
        except ValueError:
          SystemViews.errorMessage('숫자를 입력해 주세요')
          continue

  @staticmethod
  def errorMessage(message):
    print(f'[System] {message}')
    print()