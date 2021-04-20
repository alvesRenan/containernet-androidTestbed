import docker
import subprocess as sp
import shlex as sh


class ContainerNotFoundException(Exception):
  pass


FORWARD_PORTS = "sh -c '/root/port_forward.sh' & "

ANDROID_EMU_START = """sh -c 'emulator @android-22 -memory 512 -partition-size 512 -no-boot-anim -accel auto -no-window -camera-back none -camera-front none -nojni -no-cache -no-audio -qemu -vnc :2' &"""

MPOS_START = "sh -c 'java -jar mposplatform.jar' & "

def send_res(code: int, message: str) -> 'JSON':
  return { 'code': code, 'message': message }

def get_vnc(cntr_name: str) -> str:
  """
    Args:
      cntr_name: container name
    Return:
      str: the public vnc port number
  """

  "Using the Low-level API"
  d_api = docker.APIClient()
  
  """Returns a list of dicts for the running
      conatainers that have 'mn' in their names"""
  cntr_info = d_api.containers(
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
    if info.get('PrivatePort') == 5902:
      "if is VNC port then return the value of 'PublicPort'"
      return str( info.get('PublicPort') )

def exec_cmd(cmd, output=False, pipe=False):
  if output:
    return sp.getoutput( sh.split(cmd) )
  
  if pipe:
    ps = sp.Popen( cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT )
    return ps.communicate()[0]

  sp.call( sh.split(cmd) )
