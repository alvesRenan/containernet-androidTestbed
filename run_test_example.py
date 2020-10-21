import sys
from time import sleep

from android_controller.device_controller import DeviceController

"""Pass server IP and output directory"""
ctrl = DeviceController('10.0.0.12', 'out_dir')

"""Connect to the container using ADB"""
ctrl.connect_to_devices()

"""Get a list of objects that represent the containers"""
devices = ctrl.get_devices()

"""Install the app on each device"""
for android_device in devices:
  ctrl.install_app(android_device.adb_name, 'MatrixOperationsKotlin.apk')

"""Starts the app in each emulator"""
for android_device in devices:
  ctrl.start_app(
    android_device, 'com.example.renan.kotlinmpos/.MainActivity')

print('Connecting to cloudlet ....')
sleep(10)

for android_device in devices:
  ctrl.exec_activity( android_device, 
    'com.example.renan.kotlinmpos.EXTRAS', 
    "--es 'operation' 'mul' --ei 'size' 200", 5 )
