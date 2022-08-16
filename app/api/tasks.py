import os
from time import sleep
import werkzeug

from flask import request
from flask_restful import Resource, reqparse

from testbed.scnerio_creator import ScenarioCreator
from android_controller.device_controller import DeviceController
from resources.utils import *


TESTBED_CLIENT = ScenarioCreator()

parser = reqparse.RequestParser()
parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')


class HandleCreation(Resource):
  def post(self): 
    args = request.get_json()
    try:
      TESTBED_CLIENT.create_scenario( args )
      TESTBED_CLIENT.run_scenario()
      
      return send_res( 200, 'Scenario created.' )
    except Exception as e:
      return send_res( 400, 'Error creating scenario.' )


class GetStatus(Resource):
  def get(self):
    return send_res( 200, 'Running.' )


class ExecTest(Resource):
  def post(self):
    args = request.get_json()

    try:
      os.environ['TESTBED_TEST_STATUS'] = 'EXECUTING'

      controller = DeviceController( args['log_tag'] )
      controller.connect_to_devices()

      devices = controller.get_devices()
  
      for device in devices:
        print( device.adb_name )
        controller.install_app( device.adb_name, f"{APKS_FOLDER}/{args['app_name']}" )
        
      for device in devices:
        controller.start_app( device, args['main_activity'] )
        sleep(4)

        if 'run_activity' in args.keys():
          controller.exec_activity( device, args['run_activity'], args['extras'] )
      
      for device in devices:
        Thread( target=start_execution_task, args=(controller, device, args,) ).start()
        # controller.start_test( device, args['broadcast_signal'], args['arguments'], args['interactions'] )
      
      start_execution_observer( len(devices), args['interactions'] )

      return send_res( 200, 'Test execution in progress.' )
    except Exception as e:
      os.environ['TESTBED_TEST_STATUS'] = 'ERROR_ON_LAST_EXEC'

      """
        TODO: catch the exceptions
          -> some device connection erros
      """
      pass


class TestStatus(Resource):
  def get(self):
    status = os.getenv('TESTBED_TEST_STATUS')

    """if no status is available then set it to 'NOT_EXECUTING'"""
    if status is None:
      status = 'NOT_EXECUTING'
    
    """
      possible responses:
        -> NOT_EXECUTING
        -> ERROR_ON_LAST_EXEC
        -> EXECUTING
        -> FINISHED
    """

    test_info = {
      "status": status,
      "current_client_execution": MONGO_MANAGER.get_clients_current_execution()
    }

    return send_res( 200, test_info )


class StopScenario(Resource):
  def get(self):
    exec_cmd( 'mn -c' )

    return send_res( 200, 'Finished scenario execution' )


class GetVNCPort(Resource):
  def get(self, cntr_name):
    try:
      vnc_port = get_vnc_port(cntr_name)
      start_novnc( cntr_name )

      return send_res( 200, vnc_port )
    except ContainerNotFoundException:
      return send_res( 400, f'Container with name {cntr_name} not found.' )


class ManageAPKs(Resource):
  def get(self, name):
    if name == 'list':
      return send_res( 200, list_apks(), customize_msg=True, msg_name='apks' )
    
    return send_res( 404, 'Not Found' )

  def post(self, name):
    data = parser.parse_args()

    if data['file'] == '':
      return send_res( 200, 'No file found')
    
    apk = data['file']
    apk.save( os.path.join(APKS_FOLDER,name) )
    
    return send_res( 200, f'Apk {name} uploaded.' )


class ManageScenarios(Resource):
  def get(self, scenario_name):
    if scenario_name == 'list':
      data = MONGO_MANAGER.get_scenario( list_all=True )

      return send_res( 200, data, customize_msg=True, msg_name='scenarios' )

    data = MONGO_MANAGER.get_scenario( scenario_name )
    return send_res( 200, data )
  
  def post(self, scenario_name):
    scenario_info = request.get_json()

    info_msg = MONGO_MANAGER.save_scenario( scenario_name, scenario_info )

    return send_res( 200, info_msg )


class GetExecutionLogs(Resource):
  def get(self):
    return send_res( 200, MONGO_MANAGER.get_all_executions(), customize_msg=True, msg_name='execution_log' )


class CleanExecutionLogs(Resource):
  def get(self):
    MONGO_MANAGER.clean_last_execution_log()

    return send_res( 200, 'Logs deleted.' )