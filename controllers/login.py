from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user, get_jwt

from services.blocklist import BlocklistService
from services.token import TokenService

class LoginController(Resource):

    def post(self):
        json_data = request.get_json()
        # EMPTY sequences are False
        if not json_data:
            return {"message": "No username or password provided."}, 400
        
        service = TokenService(data=json_data)
        return service.user_access_token()


class RefreshController(Resource):

    # The "refresh=True" options in jwt_required to only allow refresh tokens to access this endpoint
    @jwt_required(refresh=True)
    def post(self):
        # Calling current_user will raise a RuntimeError if no @jwt.user_lookup_loader callback is defined
        data = {"username": current_user.username}
        service = TokenService(data=data)
        return service.user_refresh_token()


class LogoutController(Resource):

    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        # Calling current_user will raise a RuntimeError if no @jwt.user_lookup_loader callback is defined
        user_id = current_user.id
        username = current_user.username
        blocklist = {"jti": jti, "user_id": user_id, "username": username}
        service = BlocklistService(data=blocklist)
        return service.save_to_db()
