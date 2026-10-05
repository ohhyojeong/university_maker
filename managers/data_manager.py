import copy

from config import STATUS, CODE, DEFAULT_DATA
from .file_manager import FileManager

class DataManager:
  def __init__(self, basePath):
    self.fileManager = FileManager(basePath)

  def findAll(self, key):
    result = self.load(key)
    if result.get('status') == STATUS['ERROR']:
      return result

    return {
      'status': STATUS['SUCCESS'],
      'code': CODE['DATA_FETCHED'],
      'data': result.get('data')
    }

  def findBy(self, key, field, value):
    result = self.findAll(key)
    if result.get('status') == STATUS['ERROR']:
      return result

    for item in result.get('data') or []:
      if item.get(field) == value:
        return {
          'status': STATUS['SUCCESS'],
          'code': CODE['DATA_FETCHED'],
          'data': item
        }

    return {
      'status': STATUS['ERROR'],
      'code': CODE['DATA_NOT_FOUND'],
      'data': None
    }

  def generateId(self, data):
    ids = [
      item.get('id')
      for item in data
      if isinstance(item.get('id'), int)
    ]
    if not ids:
      return 1
    return max(ids) + 1

  def create(self, key, item):
    result = self.findAll(key)
    if result.get('status') == STATUS['ERROR']:
      return result

    data = result['data']
    
    if item.get('id') is None:
      itemId = self.generateId(data)
    else:
      itemId = int(item.get('id'))

    data.append({
      **item,
      'id': itemId,
    })

    return self.save(key, data)

  def update(self, key, itemId, fields):
    result = self.findAll(key)
    if result.get('status') == STATUS['ERROR']:
      return result
    
    data = result.get('data') or []

    for index, item in enumerate(data):
      if int(item.get('id')) == int(itemId):
        data[index] = {
          **item,
          **fields,
          'id': itemId,
        }
        return self.save(key, data)

    return {
      'status': STATUS['ERROR'],
      'code': CODE['DATA_NOT_FOUND'],
      'data': None
    }

  def delete(self, key, itemId):
    result = self.findAll(key)
    if result.get('status') == STATUS['ERROR']:
      return result

    data = result.get('data') or []
    for index, item in enumerate(data):
      if int(item.get('id')) == int(itemId):
        data.pop(index)
        return self.save(key, data)

    return {
      'status': STATUS['ERROR'],
      'code': CODE['DATA_NOT_FOUND'],
      'data': None
    }

  def save(self, key, data = None):
    if key not in DEFAULT_DATA:
      return {
        'status': STATUS['ERROR'],
        'code': CODE['UNKNOWN_KEY'],
        'data': None,
      }

    if data is None:
      result = self.load(key)
      if result.get('status') == STATUS['ERROR']:
        return result

      data = result.get('data')

    return self.fileManager.write(key, data)

  def load(self, key):
    if key not in DEFAULT_DATA:
      return {
        'status': STATUS['ERROR'],
        'code': CODE['UNKNOWN_KEY'],
        'data': None,
      }

    result = self.fileManager.read(key)

    if result.get('code') == CODE['FILE_NOT_FOUND']:
      defaultData = copy.deepcopy(DEFAULT_DATA[key])
      return self.save(key, defaultData)

    if result.get('code') == CODE['INVALID_JSON']:
      return result

    return result
