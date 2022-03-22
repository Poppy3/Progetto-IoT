from flask_restful import Api

from ..config import RESTFUL_PREFIX

api = Api(prefix=RESTFUL_PREFIX)
