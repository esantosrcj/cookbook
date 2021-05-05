from marshmallow import Schema, fields, validates, post_load, ValidationError

from models.user import User

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True, error_messages={"required": "Username is required."})
    # load_only is equivalent to "write-only"
    password = fields.Str(required=True, load_only=True)
    first_name = fields.Str(data_key="firstName")
    last_name = fields.Str(data_key="lastName")
    # dump_only is equivalent to "read-only"
    full_name = fields.Method("format_name", data_key="fullName", dump_only=True)
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        # Deserialize to an object
        return User(**data)
    
    # Validation method (inside class)
    @validates("password")
    def validate_quantity(self, value):
        if len(value) < 4:
            raise ValidationError("Password must be at least four characters long.")
    
    def format_name(self, user):
        return f"{user.last_name}, {user.first_name}"
    
    class Meta:
        ordered = True
