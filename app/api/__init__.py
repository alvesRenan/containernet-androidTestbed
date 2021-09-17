from flask_restful import Api
from app import appInstance
from .tasks import *


restful_service = Api( appInstance )

routes = [
  { 'resource': GetStatus, 'path': '/status' },
  { 'resource': HandleCreation, 'path': '/create' },
  { 'resource': StopScenario, 'path': '/stop' },
  { 'resource': ManageScenarios, 'path': '/scenarios/<string:scenario_name>' },
  { 'resource': GetVNCPort, 'path': '/vnc/<string:cntr_name>' },
  { 'resource': ManageAPKs, 'path': '/apks/<string:name>' },
  { 'resource': ExecTest, 'path': '/exec' },
  { 'resource': TestStatus, 'path': '/exec/status' },
  { 'resource': GetExecutionLogs, 'path': '/exec/logs' },
  { 'resource': CleanExecutionLogs, 'path': '/exec/clean' }
]

for route in routes:
  restful_service.add_resource( route['resource'], route['path'] )