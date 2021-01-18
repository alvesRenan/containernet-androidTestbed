import logging as log

from app import docker_ctrl
from flask import request
from flask_restful import Resource
from testbed.scnerio_creator import ScenarioCreator

from utils import *

sc = ScenarioCreator()

class HandleCreation(Resource):

  def post(self):
    log.debug('Received POST request')
    
    args = request.get_json()

    try:
      sc.create_scenario( args )
      
      send_res( 200, 'Scenario created.' )
    except:
      send_res( 400, 'Error creating scenario.' )


class GetStatus(Resource):

  def get(self):
    send_res( 200, 'Running.' )
