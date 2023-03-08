from util.constant import Constant
from db.db_connector import DbConnector

Constant.init()

with DbConnector() as c:
  print(c.test())
