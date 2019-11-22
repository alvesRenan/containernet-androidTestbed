import sys
from time import sleep

from APIs.containernet_device_manager import ContainernetDeviceManager

"Pass sserver IP and output directory"
manager = ContainernetDeviceManager('10.0.0.26', "out_dir")

"Connect to the container using ADB"
manager.connect_to_devices()

"Get a list of objects that represent the containers"
devices = manager.get_devices()

"Install the app on each device"
for android_device in devices:
  manager.install_app(android_device.adb_name, 'source-afis.apk')

"Starts the app in each emulator"
for android_device in devices:
  manager.start_app(
    android_device, 'com.example.italo.sourceafistest/.MainActivity')

print('Connecting to cloudlet ....')
sleep(5)

for android_device in devices:
  manager.exec_activity( android_device, 'sourceAfis.EXTRAS', "--es numCandidates 10000", 30 )
