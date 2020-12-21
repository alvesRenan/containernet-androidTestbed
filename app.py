import logging as log

import docker
from flask import Flask


log.basicConfig(level="DEBUG")

docker_ctrl = docker.from_env()
appInstance = Flask( __name__ )


def create_testbed():
  try:
    docker_ctrl.images.pull('renanalves/testbed-containernet')

    docker_ctrl.containers.run(
      'renanalves/testbed-containernet',
      tty=True,
      detach=True,
      name='testbed-containernet',
      pid_mode='host',
      volumes={
        '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}
      },
      privileged=True,
      command='/bin/bash'
    )
  except docker.errors.APIError:
    log.error('Image not found, container not created.')
  except docker.errors.ContainerError:
    log.error('Error starting the container.')
  except docker.errors.APIError:
    log.error('Error with docker API.')


if __name__ == "__main__":
  from threading import Thread
  
  log.debug('Creating testbed container')
  Thread(target=create_testbed).run()

  from api import *
  log.debug('Starting server')
  appInstance.run(host="0.0.0.0", debug=True)
