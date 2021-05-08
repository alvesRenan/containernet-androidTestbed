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


class SaveScenario(Resource):
  def post(self):
    pass


class ExecTest(Resource):
  def post(self):
    args = request.get_json()

    try:
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
        controller.start_test( device, args['broadcast_signal'], args['arguments'], args['interactions'] )
      
      return send_res( 200, 'Test execution in progress.' )
    except:
      """
        TODO: catch the exceptions
          -> apk not found
          -> wrong JSON format
          -> some device connection erros
      """
      pass


class StopScenario(Resource):
  def get(self):
    exec_cmd( 'mn -c' )

    return send_res( 200, 'Finished scenario execution' )


class GetVNCPort(Resource):
  def get(self, cntr_name):
    try:
      vnc_port = get_vnc_port(cntr_name)
      start_novnc( cntr_name, vnc_port )

      return send_res( 200, vnc_port )
    except ContainerNotFoundException:
      return send_res( 400, f'Container with name {cntr_name} not found.' )


class SendAPK(Resource):
  def post(self, apk_name):
    data = parser.parse_args()

    if data['file'] == '':
      return send_res( 200, 'No file found')
    
    apk = data['file']
    apk.save( os.path.join(APKS_FOLDER,apk_name) )
    
    return send_res( 200, f'Apk {apk_name} uploaded.' )
