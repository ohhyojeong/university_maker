import json
import os

from config import STATUS, CODE

class FileManager:
  def __init__(self, basePath):
    self.basePath = os.path.join(basePath, 'resources')
    os.makedirs(self.basePath, exist_ok=True)

  def filePath(self, key):
    return os.path.join(self.basePath, key + '.json')

  def write(self, key, data):
    filePath = self.filePath(key)

    with open(filePath, 'w', encoding='utf-8') as file:
      json.dump(data, file, ensure_ascii=False, indent=4)

    return {
      'status': STATUS['SUCCESS'],
      'code': CODE['DATA_SAVED'],
      'data': data
    }

  def read(self, key):
    try:
      filePath = self.filePath(key)
      with open(filePath, 'r', encoding='utf-8') as file:
        return {
          'status': STATUS['SUCCESS'],
          'code': CODE['DATA_LOADED'],
          'data': json.load(file)
        }
    except FileNotFoundError:
      return {
        'status': STATUS['ERROR'],
        'code': CODE['FILE_NOT_FOUND'],
        'data': None,
      }
    except json.JSONDecodeError:
      return {
        'status': STATUS['ERROR'],
        'code': CODE['INVALID_JSON'],
        'data': None,
      }