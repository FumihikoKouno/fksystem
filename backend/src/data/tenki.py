import pandas as pd
import datetime
import copy
from db.db_connector import DbConnector

class TenkiCrawler:
  AREA = {
    '関東・甲信': '3',
  }

  PREFECTURE = {
    '神奈川': '17',
  }

  CITY = {
    '横浜': '4610/14100'
  }

  @classmethod
  def crawl(cls, area, prefecture, city):
    #      (AREA['関東・甲信'], PREFECTURE['神奈川'], CITY['横浜'])
    url = 'https://tenki.jp/forecast/%s/%s/%s/1hour.html' % \
          (cls.AREA[area], cls.PREFECTURE[prefecture], cls.CITY[city])
    tenki_data = pd.read_html(url, index_col=0, header=2, encoding='utf-8')
    data_datetime = datetime.datetime.now()
    data_datetime = data_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    db_data = []
    for day_count in range(3):
      day_data = tenki_data[day_count].dropna(axis='index')
      for hour in range(24):
        if hour == 23:
          data_datetime = data_datetime.replace(day=data_datetime.day+1, hour=0)
        else:
          data_datetime = data_datetime.replace(hour=hour+1)
        hour_data = day_data['%02d' % (hour+1)]
        accountbook_data = DbConnector.get_data_template()
        accountbook_data['tableName'] = '気象'
        accountbook_data['value0'] = DbConnector.get_datetime_string(data_datetime)
        accountbook_data['value1'] = '神奈川県横浜市'
        accountbook_data['value2'] = hour_data['天気']
        accountbook_data['value3'] = hour_data['気温 (℃)']
        accountbook_data['value4'] = hour_data['降水確率(%)']
        accountbook_data['value5'] = hour_data['降水量 (mm/h)']
        accountbook_data['value6'] = hour_data['湿度(%)']
        accountbook_data['value7'] = hour_data['風向 風速 (m/s)'][0]
        accountbook_data['value8'] = hour_data['風向 風速 (m/s)'][1]
        db_data.append(accountbook_data)

    with DbConnector() as db:
      db.upsert(pd.DataFrame(db_data), 0, 1)
