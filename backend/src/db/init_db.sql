DROP TABLE AccountBookValues;
DROP TABLE AccountBookKeys;

CREATE TABLE AccountBookKeys (
  tableName text PRIMARY KEY,
  key0      text,
  key1      text,
  key2      text,
  key3      text,
  key4      text,
  key5      text,
  key6      text,
  key7      text,
  key8      text,
  key9      text
);

CREATE TABLE AccountBookValues (
  tableName text,
  value0    text,
  value1    text,
  value2    text,
  value3    text,
  value4    text,
  value5    text,
  value6    text,
  value7    text,
  value8    text,
  value9    text
);

INSERT
  INTO AccountBookKeys 
  (tableName, key0, key1, key2, key3, key4, key5, key6, key7, key8)
  VALUES
  ('気象', '日時', '地点', '天気', '気温 (℃)', '降水確率(%)', '降水量 (mm/h)', '湿度(%)', '風向', '風速 (m/s)');

INSERT
  INTO AccountBookKeys 
  (tableName, key0, key1, key2, key3, key4, key5, key6)
  VALUES
  ('株価', '企業名', '日付', '始値', '高値', '安値', '終値', '売買高(株)');

