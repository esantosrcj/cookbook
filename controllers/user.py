from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from extensions.jwt import jwt
from services.user import UserService
from services.blocklist import BlocklistService

class UserController(Resource):

    # This decorator sets the callback function used to convert an identity to a JSON serializable format
    # when creating JWTs
    # This is useful for using objects (such as SQLAlchemy instances) as the identity
    # when creating your tokens
    # The argument is the identity that was used when creating a JWT
    # Sets the "sub" attribute in jwt_data
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    # The decorated function can return any python object, which can then be accessed in a protected endpoint
    # If an object cannot be loaded, for example if a user has been deleted from your database, None must 
    # be returned to indicate that an error occurred loading the user
    # This is useful for automatically loading a SQLAlchemy instance based on the contents of the JWT
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_payload):
        identity = jwt_payload["sub"]
        return UserService.find_by_id_or_none(_id=identity)
    
    # Callback function to check if a JWT exists in the database blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = BlocklistService.find_by_jti(jti=jti)
        # If token exists, then return True, otherwise False
        return token is not None
    
    # This decorator sets the callback function for returning a custom response when an expired JWT is encountered
    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify(
            message="Login using username and password.",
            error="expired_token"
        ), 401
    
    # This decorator sets the callback function for returning a custom response when a valid and non-fresh token is used
    # on an endpoint that is marked as fresh=True
    @jwt.needs_fresh_token_loader
    def needs_fresh_token_response(jwt_header, jwt_payload):
        return jsonify(
            message="Resubmit username and password.",
            error="needs_fresh_token"
        ), 401
    
    # This decorator sets the callback function for returning a custom response when a revoked token is encountered
    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        return jsonify(
            message="Logged out. Login using username and password.",
            error="revoked_token"
        ), 401
    
    # This decorator sets the callback function for returning a custom response when an invalid JWT is encountered
    @jwt.invalid_token_loader
    def invalid_token_response(jwt_payload):
        return jsonify(
            message="Unable to verify token.",
            error="invalid_token"
        ), 401
    
    # This decorator sets the callback function used to return a custom response when no JWT is present
    @jwt.unauthorized_loader
    def unauthorized_response(jwt_payload):
        return jsonify(
            message="Missing access token.",
            error="unauthorized"
        ), 401


class UserListController(Resource):

    @jwt_required()
    def get(self):
        return UserService.find_all()
