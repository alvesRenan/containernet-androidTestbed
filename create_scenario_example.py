import sys
import json

from testbed.scnerio_creator import ScenarioCreator


if len( sys.argv ) != 2:
  print('Usage: python3 android_testbed.py /path/to/json_file')
  sys.exit(1)

"""Object of the class Scenario Criator."""
sc = ScenarioCreator()

"""Open the json file with the info about the scenario to be created."""
with open( sys.argv[1] ) as json_file:
  scenario_configuration = json.load( json_file )

"""Creates the nodes, interfaces and switches and connects then."""
sc.create_scenario( scenario_configuration )

"""Start the emulator on client nodes and the server on server clients, also starts the minent CLI."""
sc.run_scenario()

"""Finish the execution of the scenario and delete all containers created."""
sc.stop_scenario()
