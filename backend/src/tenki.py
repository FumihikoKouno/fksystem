import pandas as pd
import datetime
import copy
from db.db_connector import DbConnector

URL_TEMPLATE = 'https://tenki.jp/forecast/%s/%s/%s/1hour.html'

AREA = {
  '関東・甲信': '3',
}

PREFECTURE = {
  '神奈川': '17',
}

CITY = {
  '横浜': '4610/14100'
}

url = URL_TEMPLATE % (AREA['関東・甲信'], PREFECTURE['神奈川'], CITY['横浜'])

data = pd.read_html(url, index_col=0, header=2, encoding='utf-8')
today_datetime = datetime.datetime.now()
today_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
today_data = data[0].dropna(axis='index')

today_db_data = []

for hour in range(24):
  today_datetime.replace(hour=hour)
  hour_data = today_data['%02d' % (hour+1)]
  data = DbConnector.get_data_template()
  data['tablename'] = '気象'
  data['key0'] = '日時'
  data['value0'] = DbConnector.get_datetime_string(today_datetime)
  data['key1'] = '地点'
  data['value1'] = '神奈川県横浜市'
  data['key2'] = '天気'
  data['value2'] = hour_data['天気']
  data['key3'] = '気温 (℃)'
  data['value3'] = hour_data['気温 (℃)']
  data['key4'] = '降水確率(%)'
  data['value4'] = hour_data['降水確率(%)']
  data['key5'] = '降水量 (mm/h)'
  data['value5'] = hour_data['降水量 (mm/h)']
  data['key6'] = '湿度(%)'
  data['value6'] = hour_data['湿度(%)']
  data['key7'] = '風向'
  data['value7'] = hour_data['風向 風速 (m/s)'][0]
  data['key8'] = '風速 (m/s)'
  data['value8'] = hour_data['風向 風速 (m/s)'][1]
  today_db_data.append(data)

with DbConnector() as db:
  db.upsert(pd.DataFrame(today_db_data))
  print(db.get_all())
