from pymongo import MongoClient

mongo_cli = MongoClient( 'mongo', 27017 )
db = mongo_cli.testbed_db
db_collection = db.testbed_info