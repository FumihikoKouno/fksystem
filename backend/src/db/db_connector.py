import psycopg2
import pandas as pd
import copy
from util.constant import Constant

class DbConnector:

  TABLE_NAME = 'AccountBookValues'

  ACCOUNT_BOOK_DATA_TEMPLATE = {
    'tableName': None,
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
  def get_date_string(cls, date_data):
    return date_data.strftime('%Y-%m-%d')


  @classmethod
  def get_datetime_string(cls, datetime_data):
    return datetime_data.strftime('%Y-%m-%d %H:%M:%S%z')


  def get_all(self):
    self.cursor.execute('select * from AccountBookValues;')
    return pd.DataFrame(
        self.cursor.fetchall(),
        columns=list([d.name for d in self.cursor.description])
    )


  def delete(self, data):
    sql = 'DELETE FROM %s WHERE %s;'
    columns = [ column for column in data.columns ]
    for row_data in data.itertuples():
      row = [ data for data in row_data[1:] ]
      conditions = ' AND '.join([ '%s=\'%s\'' % (columns[i], row[i]) for i in range(len(row)) ])
      self.cursor.execute(sql % (DbConnector.TABLE_NAME, conditions))
      self.connection.commit()


  def upsert(self, data, *primary_nums):
    if len(primary_nums) > 0:
      delete_data = copy.deepcopy(data)
      items = [ 'value%d' % num for num in primary_nums ]
      items.append('tableName')
      delete_data = delete_data.filter(items=items, axis='columns')
      self.delete(delete_data)

    values = []
    for row in data.itertuples():
      values.append('(%s)' % ', '.join([ 'NULL' if i is None else '\'%s\'' % str(i) for i in row[1:] ]))

    sql = 'INSERT INTO %s (%s) VALUES %s;' % (DbConnector.TABLE_NAME, ', '.join(data.columns), ', '.join(values))
    self.cursor.execute(sql)
    self.connection.commit()
