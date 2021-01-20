import logging as log

from flask import request
from flask_restful import Resource
from testbed.scnerio_creator import ScenarioCreator

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