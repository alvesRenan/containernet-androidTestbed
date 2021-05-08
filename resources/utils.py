import docker
import subprocess as sp
import shlex as sh


class ContainerNotFoundException(Exception):
  pass


FORWARD_PORTS = "sh -c '/root/port_forward.sh' & "

ANDROID_EMU_START = """sh -c 'emulator @android-22 -memory 512 -partition-size 512 -no-boot-anim -accel auto -no-window -camera-back none -camera-front none -nojni -no-cache -no-audio -qemu -vnc :2' &"""

MPOS_START = "sh -c 'java -jar mposplatform.jar' & "

APKS_FOLDER = '/containernet/apks'

LAUNCH_NOVNC = '/usr/share/novnc/utils/launch.sh --vnc 0.0.0.0:5902 --listen 6080'

DOCKER_CLIENT = docker.APIClient()

TESTBED_NETWORK_ID = DOCKER_CLIENT.networks(filters={'name': 'testbed'})[0].get('Id')


def send_res(code: int, message: str) -> dict:
  return { 'code': code, 'message': message }

def get_vnc_port(cntr_name: str) -> str:
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

def exec_cmd(cmd, output=False, pipe=False, background=False):
  if pipe:
    ps = sp.Popen( cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT )
    return ps.communicate()[0]
  
  cmd = sh.split(cmd)

  if output:
    return sp.getoutput( cmd )
  
  if background:
    sp.Popen( cmd )
    return

  sp.call( cmd )

def start_novnc(cntr_name, vnc_port):
  exec_id = DOCKER_CLIENT.exec_create( f'mn.{cntr_name}', LAUNCH_NOVNC )

  try:
    DOCKER_CLIENT.exec_start( exec_id.get('Id'), detach=True )
  except:
    pass

def connect_cntr_to_network(cntr_name):
  DOCKER_CLIENT.connect_container_to_network( f'mn.{cntr_name}', TESTBED_NETWORK_ID )