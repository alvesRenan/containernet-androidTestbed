import shlex as sh
import subprocess as sp
from os import environ, listdir
from threading import Thread

import docker

from .mongo_manager import MongoManager


class ContainerNotFoundException(Exception):
  pass


FORWARD_PORTS = "sh -c '/root/port_forward.sh' & "

ANDROID_EMU_START = """sh -c 'emulator @android-22 -memory 512 -partition-size 512 -no-boot-anim -accel auto -no-window -camera-back none -camera-front none -nojni -no-cache -no-audio -qemu -vnc :2' &"""

MPOS_START = "sh -c 'java -jar mposplatform.jar' & "

APKS_FOLDER = '/containernet/apks'

LAUNCH_NOVNC = '/usr/share/novnc/utils/launch.sh --vnc 0.0.0.0:5902 --listen 6080'

DOCKER_CLIENT = docker.APIClient()

# Network Id
TESTBED_NETWORK_ID = DOCKER_CLIENT.networks(filters={'name': 'testbed'})[0].get('Id')
# Network full name
TESTBED_NETWORK_NAME = DOCKER_CLIENT.networks(filters={'name': 'testbed'})[0].get('Name')

MONGO_MANAGER = MongoManager()


def send_res(code, message, customize_msg=False, msg_name='' ):
  if customize_msg:
    return { 'code': code, msg_name: message }
  
  return { 'code': code, 'message': message }

def get_vnc_port(cntr_name):
  """
    Args:
      cntr_name: container name
    Return:
      str: the public vnc port number
  """
  
  """Returns a list of dicts for the running
      conatainers that have 'mn' in their names"""
  cntr_info = DOCKER_CLIENT.containers(
    filters={
      'name': 'mn.{}'.format(cntr_name)
    }
  )

  if cntr_info == []:
    raise ContainerNotFoundException
  
  for info in cntr_info[0].get('Ports'):
    """
      'info' -> dict {'IP': 'x.x.x.x', 'PrivatePort': xxxx, 'PublicPort': xxxx, 'Type': 'tcp'} 
    """
    if info.get('PrivatePort') == 6080:
      "if is VNC port then return the value of 'PublicPort'"
      return str( info.get('PublicPort') )

def exec_cmd(cmd, output=False, pipe=False):
  if pipe:
    ps = sp.Popen( cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT )
    return ps.communicate()[0]
  
  cmd = sh.split(cmd)

  if output:
    return sp.getoutput( cmd )

  sp.call( cmd )

def start_novnc(cntr_name):
  exec_id = DOCKER_CLIENT.exec_create( f'mn.{cntr_name}', LAUNCH_NOVNC )

  try:
    DOCKER_CLIENT.exec_start( exec_id.get('Id'), detach=True )
  except:
    pass

def connect_cntr_to_network(cntr_name):
  DOCKER_CLIENT.connect_container_to_network( f'mn.{cntr_name}', TESTBED_NETWORK_ID )

def list_apks():
  return listdir( APKS_FOLDER )

def start_execution_observer(devices_qtd, interactions):
  """
    Starts a thread to keepp cheking if the qtd of lines in mongo is 
    greater than the value of (devices_qtd * interactions)
  """

  def observer_task(num_expected_results):
    while True:
      current_results = MONGO_MANAGER.get_all_executions()

      if len(current_results) == num_expected_results:
        environ['TESTBED_TEST_STATUS'] = 'FINISHED'  
        break

  num_expected_results = devices_qtd * interactions
  Thread( target=observer_task, args=(num_expected_results,) ).start()
    
def update_cntr_cpus(cntr_name, qtd_cpus):
  sp.call( f'docker update --cpus={qtd_cpus} mn.{cntr_name}', shell=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL )

def start_execution_task(controller, device, args):
    controller.start_test( device, args['broadcast_signal'], args['arguments'], args['interactions'] )
