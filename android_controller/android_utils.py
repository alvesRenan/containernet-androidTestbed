import shlex as sh
import subprocess as sp
from threading import Thread
from time import sleep


class Android:

  def __init__(self, container_name, adb_name, out_dir):
    self.container_name = container_name
    self.adb_name = adb_name
    self.out_dir = out_dir
  
  @staticmethod
  def exec_cmd(cmd, output=False, pipe=False):
    if output:
      return sp.getoutput( sh.split(cmd) )
    
    if pipe:
      ps = sp.Popen( cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT )
      return ps.communicate()[0]

    sp.call( sh.split(cmd) )

  def start_app(self, activity, cloudlet_ip):
    """Starts App"""
    self.exec_cmd( 'adb -s %s shell am start -S %s > /dev/null' % (
      self.adb_name, activity) )

    """Define the IP of MpOS Server"""
    self.exec_cmd( "adb -s %s shell am start -n %s --es 'cloudlet' '%s' > /dev/null" % (
     self.adb_name, activity, cloudlet_ip) )
  
  def run(self, broadcast_signal, arguments, num_repetitions, random_time):
    """If random_time, then the device will wait between 1 and 5 seconds
       before it starts making the calls to the server"""
    if random_time:
      from random import randrange
      sleep( randrange(1, 5) )

    Thread( target=self.exec_run, args=(
      broadcast_signal, arguments, num_repetitions,) ).start()

  def exec_run(self, broadcast_signal, arguments, num_repetitions):
    """Clears the logcat"""
    self.exec_cmd( "adb -s %s shell logcat -c" % self.adb_name )

    current_interation = 1
    """Cicle of repetitions"""
    while current_interation <= num_repetitions:
      print( 'Interaction %i of device %s' % (current_interation, self.container_name) )

      """Send the broadcast_signal to start the activity"""
      self.exec_cmd( 'adb -s %s shell am broadcast -a %s %s > /dev/null' % (
        self.adb_name, broadcast_signal, arguments) )

      """Loop to wait for results"""
      while True:
        """Get the logcat data from the device and write
           on a file with the same name as the container"""
        self.get_results()

        try:
          """Return the number of lines in the file"""
          output = self.exec_cmd( "wc -l %s/%s | cut -f1 -d' '" % (
            self.out_dir, self.container_name), pipe=True )

          """If the number of lines is equal to the current_interaction
             then the activity has already been executed and the loop can break"""
          if int(output) == current_interation:
            current_interation += 1
            break
        
        except:
          print('sleeping')
          sleep(1)

    print( 'Executions for device %s are finished!' % self.container_name )

  def get_results(self):
    output = self.exec_cmd( 'adb -s %s shell logcat -d | grep DebugRpc > %s/%s' % (
      self.adb_name, self.out_dir, self.container_name ), pipe=True )
    
    self.exec_cmd( 'echo %s > %s/%s' % (
      output, self.out_dir, self.container_name), True )
