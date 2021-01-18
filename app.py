import logging as log
from flask import Flask


log.basicConfig(level="DEBUG")

appInstance = Flask( __name__ )


if __name__ == "__main__":

  from api import *
  log.debug('Starting server')
  appInstance.run(host="0.0.0.0", debug=True)
