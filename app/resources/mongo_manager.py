from pymongo import MongoClient


class MongoManager:

  def __init__(self) -> None:
    mongo_cli = MongoClient( 'mongodb', 27017 )
    self.scenarios = mongo_cli.scenarios
    self.executions = mongo_cli.test_db
  
  def save_scenario(self, scenario_name, scenario_conf):
    if self._scenario_exists(scenario_name):
      self.scenarios.saved_scenarios.find_one_and_update({ 'name': scenario_name }, { '$set': { 'configuration': scenario_conf } })
      return 'Scenario updated'
    
    self.scenarios.saved_scenarios.insert_one({ 'name': scenario_name, 'configuration': scenario_conf })
    return 'Scenario saved'
  
  def _scenario_exists(self, scenario_name):
    if self.scenarios.saved_scenarios.find_one({ 'name': scenario_name }) is None:
      return False
    
    return True
  
  def get_scenario(self, scenario_name=None, list_all=False):
    if list_all:
      scenarios = []
      for i in self.scenarios.saved_scenarios.find({}, { '_id': False }):
        scenarios.append( i )
      
      return scenarios

    if self._scenario_exists(scenario_name):
      data = self.scenarios.saved_scenarios.find_one({ 'name': scenario_name })

      return data.get('configuration')
    
    return 'Scenario not found.'
  
  def get_all_executions(self):
    results = []
    for i in self.executions.execution_log.find( { 'execution_number': {'$gt': 0} }, {'_id': False} ):
      results.append( i )
    
    return results
  
  def clean_last_execution_log(self):
    self.executions.execution_log.drop()
  
  def get_clients_current_execution(self):
    pipeline = [
      { 
        "$group": {
          "_id": "$device_name",
          "max_exec": { "$max": "$execution_number" }
        }
      },
      { 
        "$project": {
          "device": "$_id",
          "current_interaction": "$max_exec",
          "_id": 0
        }
      }
    ]

    return list( self.executions.execution_log.aggregate(pipeline) )
