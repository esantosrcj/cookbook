from marshmallow import Schema, fields, validates, post_load, ValidationError

from models.ingredient import Ingredient

class IngredientSchema(Schema):
    # dump_only is equivalent to "read-only"
    id = fields.Int()
    name = fields.Str(required=True, error_messages={"required": "Name is required."})
    quantity = fields.Int(required=True)


    # Pass class name as a string to avoid circular imports (RecipeSchema located in a different module)

    # only
    #   Explicitly specify which attributes of the nested objects you want to (de)serialize with the 'only' 
    #   argument to the schema
    # Example:
    #   recipe = fields.Nested("RecipeSchema", only=("name", "created_at"))

    # data_key
    #   If you are consuming and producing data that does not match your schema, you can specify the output
    #   keys via the 'data_key' argument
    # Example:
    #   recipe_id = fields.Int(required=True, data_key="recipeId")
    #   dump/serialize: { 'recipeId': 1 }
    #   load/deserialize: { 'recipe_id': 1 }
    #recipe_id = fields.Nested("RecipeSchema", only=("id",), data_key="recipeId")
    recipe_id = fields.Int(required=True, data_key="recipeId")

    # marshmallow.decorators.post_load
    #   Register a method to invoke after deserializing an object
    @post_load
    def make_ingredient(self, data, **kwargs):
        # Deserialize to an object
        return Ingredient(**data)

    # Validation method (inside class)
    @validates("quantity")
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than 0.")
    
    class Meta:
        ordered = True
