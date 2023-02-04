import psycopg2
import pandas as pd
from util.constant import Constant

class DbConnector:

  def __init__(self):
    self.url = Constant.get('database', 'url')
    self.port = Constant.get('database', 'port')
    self.user = Constant.get('database', 'user')
    self.password = Constant.get('database', 'password')
    self.name = Constant.get('database', 'name')


  def __enter__(self):
    self.connection = psycopg2.connect(
      'dbname=%s host=%s port=%s user=%s password=%s' % 
      (self.name, self.url, self.port, self.user, self.password)
    )
    self.cursor = self.connection.cursor()
    return self


  def __exit__(self, e_type, e_value, traceback):
    self.cursor.close()
    self.connection.close()


  def test(self):
    self.cursor.execute('select age, name from test;')
    return pd.DataFrame(
        self.cursor.fetchall(),
        columns=list([d.name for d in self.cursor.description])
    )
