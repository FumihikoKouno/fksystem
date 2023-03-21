from fastapi import FastAPI
#from api.db.db_api import DbApi
from api.db.db_api import DbApi

app = FastAPI()

@app.middleware('http')
async def add_my_headers(request, call_next):
  response = await call_next(request)
  response.headers['Access-Control-Allow-Origin'] = '*'
  return response

@app.get('/test/{id}/{name}')
async def root(id, name):
  return {'message': f'hello World {id} : {name}'}

@app.get('/data/list')
async def get_data_list():
  return DbApi.get_data_list()
