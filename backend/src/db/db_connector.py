import psycopg2
import pandas as pd
import copy
from util.constant import Constant

class DbConnector:

  ACCOUNT_BOOK_DATA_TEMPLATE = {
    'tablename': None,
    'key0': None, 'key1': None, 'key2': None, 'key3': None, 'key4': None,
    'key5': None, 'key6': None, 'key7': None, 'key8': None, 'key9': None,
    'value0': None, 'value1': None, 'value2': None, 'value3': None, 'value4': None,
    'value5': None, 'value6': None, 'value7': None, 'value8': None, 'value9': None,
  }

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


  @classmethod
  def get_data_template(cls):
    return copy.deepcopy(cls.ACCOUNT_BOOK_DATA_TEMPLATE)


  @classmethod
  def get_datetime_string(cls, datetime_data):
    return datetime_data.strftime('%Y-%m-%d %H:%M:%S%z')


  def get_all(self):
    self.cursor.execute('select * from AccountBook;')
    return pd.DataFrame(
        self.cursor.fetchall(),
        columns=list([d.name for d in self.cursor.description])
    )


  def upsert(self, data):
    values = []
    for row in data.itertuples():
      values.append('(%s)' % ', '.join([ 'NULL' if i is None else '\'%s\'' % str(i) for i in row[1:] ]))

    sql = 'INSERT INTO AccountBook (%s) VALUES %s;' % (', '.join(data.columns), ', '.join(values))
    print(sql)
    self.cursor.execute(sql)
    self.connection.commit()
