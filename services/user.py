import datetime as dt

from passlib.hash import bcrypt

from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from extensions.db import db
from models.user import User
from schemas.user import UserSchema

user_schema = UserSchema(exclude=("id", "created_at"))

class UserService:

    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return f"<UserService >"
    
    @classmethod
    def find_all(cls):
        users = User.query.all()
        # dump/serialize
        users_result = UserSchema(many=True, only=("username", "full_name")).dump(users)
        return users_result

    @classmethod
    def find_by_id_or_none(cls, _id):
        return User.query.filter_by(id=_id).one_or_none()
    
    def signup_user(self):
        # Validate and deserialize
        try:
            # load/deserialize to User object
            user = user_schema.load(self.data)
        except ValidationError as err:
            return err.messages, 400

        all_users = User.query.all()
        all_usernames_lower = [u.username.lower() for u in all_users]
        # TODO: Check all emails

        if user.username.lower() in all_usernames_lower:
            return {"message": "Username already exists."}, 400
        
        pwd_hash = bcrypt.hash(user.password)
        user.password = pwd_hash
        user.created_at = dt.datetime.now()
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable to add user account."}, 500
        
        # dump/serialize
        user_result = user_schema.dump(User.query.get(user.id))
        return {"message": "Created new user account.", "user": user_result}
