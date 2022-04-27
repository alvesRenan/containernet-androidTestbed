import shlex as sh
import subprocess as sp

import docker

from android_controller.android_utils import Android
from resources.utils import TESTBED_NETWORK_NAME


class DeviceController:

  def __init__(self, log_tag):
    """
      Args:
        log_tag (str): tag used to get search for results in the device log
    """
    self.containers = []
    self.log_tag = log_tag

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
    for cntr_info in mn_containers:
      "Split retuns: '/' + 'conainer_name'"
      _, name = cntr_info.get('Names')[0].split('/')
       
      """If container exposes port 5555, then host_port is a list
         with a dict containing the keys 'HostIp' and 'HostPort'"""
      host_port = d_api.port(name,5555)
      
      """If host_port is None, it means the container 
         is not running a emulator"""
      if host_port != None:
        "Dict with 'HostIp' and 'HostPort' of a given container"
        cntr_ip = cntr_info.get('NetworkSettings').get('Networks').get(TESTBED_NETWORK_NAME).get('IPAddress')
        adb_name = f"{cntr_ip}:5555"
        
        "Add to use on the get_devices method"
        self.containers.append( (name, adb_name) )

        "Mount the correct 'adb connect' command"
        cmd = f"adb connect {adb_name}"

        "Exec the shell command"
        sp.call( sh.split(cmd) )
  
  def get_devices(self):
    """
      Creates an object of the Android class for each client container 

      Returns:
        list of Android objects
    """

    devices = []

    for name, adb_name in self.containers:
      android_device = Android(name, adb_name, self.log_tag)
      devices.append(android_device)
    
    return devices
  
  @staticmethod
  def install_app(adb_name, path_to_app):
    """
      Install an app in an emulator

      Args:
        adb_name (str): name representation of the emulator on the adb list
        path_to_app (str): path to the APK file
    """

    cmd = "adb -s %s install -r -t %s" % (adb_name, path_to_app)

    sp.call( sh.split(cmd) )
  
  @staticmethod
  def start_app(android_obj, activity):
    """
      Calls the start_app method of a given Android object

      Args:
        android_obj (Android): Android class object
        activity (str): Name of the app activity to be called

      Output:
        Prints the name of the container where the app was started
    """

    android_obj.start_app (activity )
  
  @staticmethod
  def exec_activity(android_obj, activity, extras):
    """
      Executes a new activity without closing a existing one

      Args:
        android_obj (Android): Android class object
        activity (str): Name of the app activity to be called

      Output:
        Prints the name of the container where the app was started
    """
    android_obj.run_activity( activity, extras )

  @staticmethod
  def start_test(android_obj, broadcast_signal, arguments, num_repetitions):
    """
      Starts a Thread for the Android object and keep sending the broadcast_signal until num_repetitions is hit

      Args:
        android_obj (Android): Android class object
        broadcast_signal (str): A flag that will trigger a broadcast receiver 
                                in the app to start the activity that should 
                                be executed
        arguments (str): Arguments to be passed to the activity via Intent
        num_repetitions (int): Number of times the activity will be execcuted
    """
    android_obj.run(broadcast_signal, arguments, num_repetitions)
