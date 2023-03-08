import configparser 

class Constant:

  FILE_NAME = 'setting.ini'

  @classmethod
  def init(cls):
    cls.config = configparser.ConfigParser()
    cls.config.read(cls.FILE_NAME)

  @classmethod
  def get(cls, section, key):
    if not hasattr(cls, 'config'):
      cls.init()
    return cls.config.get(section, key)
  
