import logging as log
from flask import Flask
from flask_cors import CORS


log.basicConfig(level="INFO")

appInstance = Flask( __name__ )
CORS(appInstance)

if __name__ == "__main__":

  from api import *
  log.debug('Starting server')
  appInstance.run(host="0.0.0.0", debug=True)
