"""
  This file must be executed inside the containernet container
  using Python Version 3. Make sure to install the 'docker' dependece.
"""

import json

from APIs.scnerio_creator import ScenarioCreator

"Object of the class Scenario Criator."
sc = ScenarioCreator()

"Open the json file with the info about the scenario to be created."
with open('example.json') as j_file:
  "Load the json file as a dict."
  data = json.load( j_file )

"Creates the nodes, interfaces and switches and connects then."
sc.create_scenario( data )

"Start the emulator on client nodes and the server on server clients, also starts the minent CLI."
sc.run_scenario()

"Finish the execution of the scenario and delete all containers created."
sc.stop_scenario()
