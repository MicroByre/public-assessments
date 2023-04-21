"""µByre example service"""
__version__=(0,1,0)
__author__='Alex Miłowski'
__author_email__='alex@microbyre.com'

import sys
import os
import logging

from .config import Config, get_config
from .service import service

def set_loglevel(log_level):
   if log_level is not None:
      n_log_level = getattr(logging, log_level.upper(), None)
      if n_log_level is not None:
         logging.basicConfig(level=n_log_level)

__configured__ = None
if 'SERVICE_CONFIG' in os.environ and __configured__ is None:
   # FYI: if you call logging before configuration, the level won't be set properly. Thus, we use print
   config_value = os.environ['SERVICE_CONFIG']
   print(f'Loading configuration from: {config_value}')
   modulename, _, classname = os.environ['SERVICE_CONFIG'].rpartition('.')
   print(f'\tmodule: {modulename}')
   print(f'\t class: {classname}')


   try:
      m = __import__(modulename)
      if not hasattr(m,classname):
         logging.error(f'Module {modulename} does not have a class named {classname}')
         sys.exit(1)
      config = getattr(m,classname)()
      service.config.from_object(config)
      __configured__ = {
         'module' : modulename,
         'class' : classname,
         'instance' : config
      }
      service.config['SWAGGER'] = {
         'openapi': '3.0.2',
         'info' : {
            'version' : 'v'+'.'.join(map(str,__version__)),
            'title' : 'automaton'
         }
      }
      with service.app_context():
         log_level = get_config('LOG_LEVEL')
         if log_level is not None:
            set_loglevel(log_level)

   except ModuleNotFoundError as ex:
      logging.exception(ex)
      logging.error(f'Error loading module {modulename}')
      sys.exit(1)
else:
   with service.app_context():
      log_level = get_config('LOG_LEVEL')
      if log_level is not None:
         set_loglevel(log_level)
