from flask_restful import Api
from app import appInstance
from .tasks import *


restful_service = Api( appInstance )

routes = [
  { 'resource': GetStatus, 'path': '/status' },
  { 'resource': HandleCreation, 'path': '/create' },
  { 'resource': SaveScenario, 'path': '/save' },
  { 'resource': ExecTest, 'path': '/exec' },
  { 'resource': GetVNCPort, 'path': '/vnc/<string:cntr_name>' },
  { 'resource': SendAPK, 'path': '/send-apk/<string:apk_name>' },
  { 'resource': StopScenario, 'path': '/stop' }
]

for route in routes:
  restful_service.add_resource( route['resource'], route['path'] )