from flask_restful import Api
from app import appInstance
from .tasks import *


restful_service = Api( appInstance )

restful_service.add_resource(GetStatus, '/status')
restful_service.add_resource(HandleCreation, '/create')