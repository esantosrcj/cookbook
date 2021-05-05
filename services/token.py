from passlib.hash import bcrypt

from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError

from models.user import User
from schemas.token import TokenSchema

token_schema = TokenSchema()

class TokenService:

    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return f"<TokenService >"

    def user_access_token(self):
        # Validate and deserialize
        try:
            # load/deserialize to OrderedDict
            token_data = token_schema.load(self.data)
        except ValidationError as err:
            return err.messages, 400

        username = token_data["username"]
        password = token_data["password"]
        user = User.query.filter_by(username=username).one_or_none()
        if not user or not bcrypt.verify(password, user.password):
            return {"message": "Invalid username or password."}, 401

        # Return a "fresh" access token
        token_data["access_token"] = create_access_token(identity=user, fresh=True)
        token_data["refresh_token"] = create_refresh_token(identity=user)

        # dump/serialize
        token_result = token_schema.dump(token_data)
        return token_result
    
    def user_refresh_token(self):
        username = self.data["username"]
        user = User.query.filter_by(username=username).one_or_none()
        # If we are refreshing a token here, we have not verified the users password in a while,
        # so mark the newly created access token as not fresh
        new_token = create_access_token(identity=user, fresh=False)
        token_data = {"access_token": new_token}
        # dump/serialize
        token_result = token_schema.dump(token_data)
        return token_result


