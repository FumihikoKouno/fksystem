import pandas as pd
import datetime
from db.db_connector import DbConnector

# 定数定義
url='https://kabutan.jp/stock/kabuka?code=%s&ashi=day&page=%d'

code=4004
db_data = []
for page in range(10):
  data = pd.read_html(url % (code, page+1), header=0, encoding='utf-8')[5].T
  for day in data.columns:
    day_data = data[day]
    accountbook_data = DbConnector.get_data_template()
    accountbook_data['tableName'] = '株価'
    accountbook_data['value0'] = '企業名'
    accountbook_data['value1'] = DbConnector.get_date_string(
        datetime.datetime.strptime(day_data['日付'], '%y/%m/%d')
    )
    accountbook_data['value2'] = day_data['始値']
    accountbook_data['value3'] = day_data['高値']
    accountbook_data['value4'] = day_data['安値']
    accountbook_data['value5'] = day_data['終値']
    accountbook_data['value6'] = day_data['売買高(株)']
    db_data.append(accountbook_data)

with DbConnector() as db:
  db.upsert(pd.DataFrame(db_data), 0, 1)





