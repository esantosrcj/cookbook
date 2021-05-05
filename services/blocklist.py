import datetime as dt

from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from extensions.db import db
from models.blocklist import TokenBlocklist
from schemas.blocklist import BlocklistSchema

blocklist_schema = BlocklistSchema()

class BlocklistService:

    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return f"<BlocklistService >"

    @classmethod
    def find_by_jti(cls, jti):
        # Return the first element of the first result or None if no rows present
        return TokenBlocklist.query.filter_by(jti=jti).scalar()
    
    def save_to_db(self):
        # Validate and deserialize
        try:
            # load/deserialize to TokenBlocklist object
            token_blocklist = blocklist_schema.load(self.data)
        except ValidationError as err:
            return err.messages, 400

        token_blocklist.created_at = dt.datetime.now()
        try:
            db.session.add(token_blocklist)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable to logout successfully."}, 500

        # dump/serialize
        blocklist_result = blocklist_schema.dump(TokenBlocklist.query.get(token_blocklist.id))
        return {"message": "User logged out.", "tokenBlocklist": blocklist_result}