from marshmallow import Schema, fields, validates, ValidationError

class TokenSchema(Schema):
    username = fields.Str(required=True, load_only=True, error_messages={"required": "Username is required."})
    # load_only is equivalent to "write-only"
    password = fields.Str(required=True, load_only=True, error_messages={"required": "Password is required."})
    access_token = fields.Str(dump_only=True, data_key="accessToken")
    refresh_token = fields.Str(dump_only=True, data_key="refreshToken")
    
    # Validation method (inside class)
    @validates("password")
    def validate_quantity(self, value):
        if len(value) < 4:
            raise ValidationError("Password must be at least four characters long.")
    
    class Meta:
        ordered = True
