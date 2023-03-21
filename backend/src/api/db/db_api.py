from db.db_connector import DbConnector

class DbApi():
  
  @classmethod
  def get_data_list(cls):
    with DbConnector() as db:
      return db.get_data_list().to_json(
          orient='split',
          index=False,
          force_ascii=False
      )
