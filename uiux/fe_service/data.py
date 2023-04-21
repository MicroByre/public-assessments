import os
from glob import glob

from flask import Blueprint, send_from_directory, jsonify

from .message import StatusResponse, StatusCode, ServiceInfo
from .config import get_data_dir
from . import __version__

data_access = Blueprint('data', __name__, url_prefix='/data')

@data_access.route('/')
def service_info():
   """
   Returns the service information metadata
   """
   return jsonify(
      ServiceInfo(
         version=f'v{".".join(map(str,__version__))}',
         libraries={},
         message='Howdy!'))

@data_access.route('/<kind>')
def items(kind):
   """
   Returns a list of data objects by kind
   """
   dir = os.path.join(get_data_dir(),kind)
   if not os.path.exists(dir):
      return jsonify(
         StatusResponse(
            message=f'Kind {kind} does not exist.', 
            status=StatusCode.Error)), 404
   if not os.path.isdir(dir):
      return jsonify(
         StatusResponse(
            message=f'Kind {kind} is not valid.',
            status=StatusCode.Error)), 400
   
   items = [ item.rpartition('/')[2].rpartition('.')[0] for item in glob(os.path.join(dir,'*.json'))]
   return jsonify(items)

@data_access.route('/<kind>/<item>')
def data_item(kind,item):
   """
   Returns a specific data object by kind and name
   """
   dir = get_data_dir()
   path = os.path.join(kind,item+'.json')
   if os.path.exists(os.path.join(dir,path)):
      return send_from_directory(dir, path)
   else:
      return jsonify(
         StatusResponse(
            message=f'{kind}/{item} does not exist.', 
            status=StatusCode.Error)), 404
