import shlex as sh
import subprocess as sp

import docker

from APIs.android_utils import Android


class ContainernetDeviceManager:

  def __init__(self, cloudlet_ip, out_dir):
    """
      Args:
        cloudlet_ip: IP of the container running the MpOS server
        out_dir: directory where the log files will be dumped
    """
    self.cloudlet_ip = cloudlet_ip
    self.containers = []
    self.out_dir = out_dir

    "Create out_dir"
    sp.call(['mkdir', self.out_dir])

  def connect_to_devices(self):
    """
      Connects to the android emulators in the client containers
    """

    "Using the Low-level API"
    d_api = docker.APIClient()
    
    """Returns a list of dicts for the running
       conatainers that have 'mn' in their names"""
    mn_containers = d_api.containers(
      filters={
        "name": "mn"
      }
    )

    "Loop through the dicts"
    for container_info in mn_containers:
      "Split retuns: '/' + 'conainer_name'"
      _, name = container_info.get('Names')[0].split('/')
       
      """If container exposes port 5555, then host_port is a list
         with a dict containing the keys 'HostIp' and 'HostPort'"""
      host_port = d_api.port(name,5555)
      
      """If host_port is None, it means the container 
         is not running a emulator"""
      if host_port != None:
        "Dict with 'HostIp' and 'HostPort' of a given container"
        d = host_port[0]

        adb_name = "%s:%s" % ( d.get('HostIp'), d.get('HostPort') )
        
        "Add to use on the get_devices method"
        self.containers.append( (name, adb_name) )

        "Mount the correct 'adb connect' command"
        cmd = "adb connect %s" % adb_name 

        "Exec the shell command"
        sp.call( sh.split(cmd) )
  
  def get_devices(self):
    """
      For each client container creates an object of the Android class

      Returns:
        List of Android objects
    """

    devices = []

    for name, adb_name in self.containers:
      android_device = Android(name, adb_name, self.out_dir)
      devices.append(android_device)
    
    return devices
  
  @staticmethod
  def install_app(adb_name, path_to_app):
    """
      Install an app in an emulator

      Args:
        adb_name: name representation of the emulator on the adb list
        path_to_app: path or name, with in the same folder, of the app
    """

    cmd = "adb -s %s install -r -t %s" % (adb_name, path_to_app)

    sp.call( sh.split(cmd) )
  
  def start_app(self, android_obj, activity):
    """
      Calls the start_app method of a given Android object

      Args:
        android_obj: Android class object
        activity: Name of the app activity to be called

      Output:
        Prints the name of the container where the app was started
    """

    android_obj.start_app(activity, self.cloudlet_ip)
    print( "Stated activity %s on device %s" % (activity, android_obj.container_name) )

  def exec_activity(self, android_obj, broadcast_signal, arguments, num_repetitions, random_time=False):
    """
      Starts a Thread for the Android object and keep sending the broadcast_signal until num_repetitions is hit

      Args:
        android_obj: Android class object
        broadcast_signal: A flag that will trigger a broadcast receiver in the app to start the activity that should be executed
        arguments: Arguments to be passed to the activity via Intent
        num_repetitions: Number of times the activity will be execcuted
        random_time: Defines if the emulators will wait a random time before starting the activity
    """
    android_obj.run(broadcast_signal, arguments, num_repetitions, random_time)
