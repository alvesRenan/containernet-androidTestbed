import logging as log

from flask import request
from flask_restful import Resource

from testbed.scnerio_creator import ScenarioCreator
from android_controller.device_controller import DeviceController
from resources.utils import *


sc = ScenarioCreator()


class HandleCreation(Resource):
  def post(self):
    log.debug('Received POST request')
    
    args = request.get_json()
    try:
      sc.create_scenario( args )
      sc.run_scenario()
      
      return send_res( 200, 'Scenario created.' )
    except:
      return send_res( 400, 'Error creating scenario.' )


class GetStatus(Resource):
  def get(self):
    return send_res( 200, 'Running.' )


class SaveScenario(Resource):
  def post(self):
    pass


class ExecTest(Resource):
  def post(self):
    log.debug( 'Received POST request' )
    
    args = request.get_json()
    try:
      controller = DeviceController()
      devices = controller.connect_to_devices()
  
      for device in devices:
        controller.install_app( device, args['app_name'] )

      for device in self.devices:
        controller.start_app( device, args['main_activity'] )

        if 'run_activity' in args.keys():
          controller.exec_activity( device, args['extra_activity'], args['extras'] )
      
      for device in devices:
        controller.start_test( device, args['broadcast_signal'], args['arguments'], args['interactions'] )

    except:
      pass
