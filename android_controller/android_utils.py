from threading import Thread
from time import sleep
from datetime import datetime

import pymongo
from resources.utils import exec_cmd


class Android:

  def __init__(self, device_name, adb_name, log_tag):
    self.device_name = device_name
    self.adb_name = adb_name
    self.log_tag = log_tag

    self.mongo_cli = pymongo.MongoClient('mongodb', 27017)
    self.db = self.mongo_cli.test_db

  def run(self, broadcast_signal, arguments, num_repetitions):
    sleep(5) #TODO: find a better solution than sleep

    Thread( target=self.exec_run, args=(
      broadcast_signal, arguments, num_repetitions,) ).start()
  
  def start_app(self, activity):
    """Starts App"""
    exec_cmd( f'adb -s {self.adb_name} shell am start -S {activity} > /dev/null' )

  def run_activity(self, activity, args=''):
    """Opens new activity"""
    exec_cmd( f"adb -s {self.adb_name} shell am start -n {activity} '{args}' > /dev/null" )

  def exec_run(self, broadcast_signal, arguments, num_repetitions):
    """Clears the logcat"""
    exec_cmd( f'adb -s {self.adb_name} shell logcat -c' )

    """Creat entry number 0 for the device"""
    self.db.execution_log.insert_one({ 'device_name': self.device_name, 'log': '', 'execution_number': 0 })

    current_interation = 1
    """Cicle of repetitions"""
    while current_interation <= num_repetitions:
      """Send the broadcast_signal to start the activity"""
      exec_cmd( f'adb -s {self.adb_name} shell am broadcast -a {broadcast_signal} {arguments} > /dev/null' )

      """Loop to wait for results"""
      while True:
        """Get the logcat data from the device and saves on a mongodb collection"""
        self.get_results(current_interation)

        """try find an entry with the device name and the current execution number"""
        last_recorded_execution = self.db.execution_log.find_one({ 'device_name': self.device_name, 'execution_number': current_interation })
        
        """if a entry is found the current execution is completed"""
        if last_recorded_execution is not None:

          """update the current_interation and break the loop"""
          current_interation += 1
          break
        
        """if no entry is found, sleep and try again"""
        sleep(1)

  def get_results(self, current_interation):
    """last recorded log line"""
    if current_interation == 1:
      last_saved_log = self.db.execution_log.find_one({ 'device_name': self.device_name, 'execution_number': 0 })
    else:
      last_saved_log = self.db.execution_log.find_one({ 'device_name': self.device_name, 'execution_number': current_interation-1 })
    
    if last_saved_log is not None:
      """get last execution log entry"""
      last_log_line = exec_cmd( f'adb -s {self.adb_name} shell logcat -d | grep {self.log_tag} | tail -n 1', pipe=True )
      last_log_line = last_log_line.decode("utf-8") 

      if last_log_line != last_saved_log.get('log') and last_log_line != '':
        """save on mongodb"""
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.db.execution_log.insert_one({ 'device_name': self.device_name, 'log': last_log_line, 'execution_number': current_interation, 'timestamp': timestamp })
