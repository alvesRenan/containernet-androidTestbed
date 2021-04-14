from flask_restful import Api
from app import appInstance
from .tasks import *


restful_service = Api( appInstance )

routes = [
  { 'resource': GetStatus, 'path': '/status' },
  { 'resource': HandleCreation, 'path': '/create' },
  { 'resource': SaveScenario, 'path': '/save' },
  { 'resource': ExecTest, 'path': '/exec' }
]

for route in routes:
  restful_service.add_resource( route['resource'], route['path'] )