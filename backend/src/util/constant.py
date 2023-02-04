import configparser 

class Constant:

  @classmethod
  def init(cls, file_name):
    cls.config = configparser.ConfigParser()
    cls.config.read(file_name)

  @classmethod
  def get(cls, section, key):
    return cls.config.get(section, key)
  
