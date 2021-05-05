from flask import request
from flask_restful import Resource

from services.user import UserService

class SignupController(Resource):

    def post(self):
        json_data = request.get_json()
        # EMPTY sequences are False
        if not json_data:
            return {"message": "No user data provided."}, 400
        
        service = UserService(data=json_data)
        return service.signup_user()
