import json

from APIs.scnerio_creator import ScenarioCreator

sc = ScenarioCreator()

with open('example.json') as j_file:
  data = json.load( j_file )

sc.create_scenario( data )

sc.run_scenario()

sc.stop_scenario()
