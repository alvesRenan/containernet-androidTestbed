from pymongo import MongoClient


class MongoManager:

  def __init__(self) -> None:
    mongo_cli = MongoClient( 'mongodb', 27017 )
    self.db = mongo_cli.scenarios
  
  def save_scenario(self, scenario_name, scenario_conf):
    if self._scenario_exists(scenario_name):
      self.db.saved_scenarios.find_one_and_update({ 'name': scenario_name }, { '$set': { 'configuration': scenario_conf } })
      return 'Scenario updated'
    
    self.db.saved_scenarios.insert_one({ 'name': scenario_name, 'configuration': scenario_conf })
    return 'Scenario saved'
  
  def _scenario_exists(self, scenario_name):
    if self.db.saved_scenarios.find_one({ 'name': scenario_name }) is None:
      return False
    
    return True
  
  def get_scenario(self, scenario_name):
    if self._scenario_exists(scenario_name):
      data = self.db.saved_scenarios.find_one({ 'name': scenario_name })

      return data.get('configuration')
    
    return 'Scenario not found.'