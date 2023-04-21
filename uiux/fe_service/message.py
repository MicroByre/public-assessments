from pydantic import BaseModel
from enum import Enum
from typing import Any, Dict

class StatusCode(Enum):
   Success = 'Success'
   Error = 'Error'
   Unavailable = 'Unavailable'

class StatusResponse(BaseModel):
   status: StatusCode = StatusCode.Success
   message: str = ''
   data: Any = None

class ServiceInfo(BaseModel):
   version: str
   libraries: Dict[str, str]
   message: str = ''
