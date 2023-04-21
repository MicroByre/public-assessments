import importlib.resources
import logging
from datetime import date, datetime
import enum
import json

from pydantic import BaseModel
from flask import Flask, send_from_directory

from .config import Config
from .data import data_access

import fe_service

with importlib.resources.as_file(importlib.resources.files(fe_service).joinpath('frontend')) as path:
   frontend_dir = str(path)

logging.info(f'Loading static site from {frontend_dir}')

service = Flask('µ',static_url_path='',static_folder=frontend_dir)
service.config.from_object(Config())

service.register_blueprint(data_access)

class ModelEncoder(json.JSONEncoder):
   def default(self, obj):
      if isinstance(obj,enum.Enum):
         return obj.value
      if isinstance(obj, (datetime, date)):
         return obj.isoformat()
      if isinstance(obj,BaseModel):
         return obj.dict(exclude_none=True,exclude={'_id'})
      return super().default(obj)

service.json_encoder = ModelEncoder

@service.route('/')
def index():
   return send_from_directory(frontend_dir, 'index.html')
