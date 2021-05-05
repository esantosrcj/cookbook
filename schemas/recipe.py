from marshmallow import Schema, fields, validates, ValidationError

class RecipeSchema(Schema):
    # dump_only is equivalent to "read-only"
    id = fields.Int()
    name = fields.Str(required=True)

    # Pass class name as a string to avoid circular imports (IngredientSchema located in a different module)

    # only
    #   Explicitly specify which attributes of the nested objects you want to (de)serialize with the 'only' 
    #   argument to the schema
    ingredients = fields.List(fields.Nested("IngredientSchema", only=("id", "name", "quantity")), missing=[])

    # Validation method (inside class)
    @validates("name")
    def validate_name(self, value):
        if not value:
            raise ValidationError("Name is required")
    
    class Meta:
        ordered = True
