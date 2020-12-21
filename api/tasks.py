import logging as log

from flask import request
from flask_restful import Resource

from app import docker_ctrl


class HandleCreation(Resource):

  def post(self):
    log.debug('Received POST request')
    
    args = request.get_json()
    return args,200


class GetStatus(Resource):

  def get(self):
    try:
      cntr = docker_ctrl.containers.get('testbed-containernet')

      if cntr.status == 'running':
        return {'status': 'running'}
    except:
      pass
    
    return {'status': 'not running'}