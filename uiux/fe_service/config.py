
import os

from flask import current_app

class Config:
   DATA_DIR='data'

def get_config(name,default=None):
   return os.environ.get(name,current_app.config.get(name,default))

def get_data_dir():
   return get_config('DATA_DIR','data')