from marshmallow import Schema, fields, validate, validates, post_load, ValidationError

from models.blocklist import TokenBlocklist

class BlocklistSchema(Schema):
    id = fields.Int()
    jti = fields.Str(required=True, error_messages={"required": "JTI is required."})
    user_id = fields.Int(required=True)
    username = fields.Str(required=True, error_messages={"required": "Username is required."})
    created_at = fields.DateTime()

    # marshmallow.decorators.post_load
    #   Register a method to invoke after deserializing an object
    @post_load
    def make_token_blocklist(self, data, **kwargs):
        # Deserialize to an object
        return TokenBlocklist(**data)

    # Validation method (inside class)
    @validates("user_id")
    def validate_user_id(self, value):
        if value < 1:
            raise ValidationError("A user ID is required.")
    
    class Meta:
        ordered = True
