from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from extensions.db import db
from models.recipe import Recipe
from models.ingredient import Ingredient
from schemas.ingredient import IngredientSchema

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)

class IngredientService:

    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return f"<IngredientService >"
    
    @classmethod
    def find_all(cls):
        ingredients = Ingredient.query.order_by(Ingredient.id.asc()).all()
        # dump/serialize
        ingredients_result = ingredients_schema.dump(ingredients)
        return ingredients_result

    @classmethod
    def find_by_id(cls, _id):
        ingredient = Ingredient.query.get(_id)
        if ingredient:
            # dump/serialize
            ingredient_result = ingredient_schema.dump(ingredient)
            return ingredient_result
        
        return {"message": "Ingredient could not be found."}, 404

    def save_to_db(self):
        # Validate and deserialize
        try:
            # load/deserialize to Ingredient object
            ingredient = ingredient_schema.load(self.data)
        except ValidationError as err:
            return err.messages, 400
        
        recipe = Recipe.query.get(ingredient.recipe_id)
        if recipe is None:
            return {"message": "Recipe could not be found for ingredient."}, 400

        if ingredient.name.lower() in [i.name.lower() for i in recipe.ingredients]:
            return {"message": "Ingredient already exists in recipe."}, 400

        try:
            db.session.add(ingredient)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable add ingredient."}, 500

        # dump/serialize
        ingredient_result = ingredient_schema.dump(Ingredient.query.get(ingredient.id))
        return {"message": "Created new ingredient.", "ingredient": ingredient_result}
    
    def update_in_db(self):
        # Validate and deserialize
        try:
            # load/deserialize to Ingredient object
            ingredient_data = ingredient_schema.load(self.data)
        except ValidationError as err:
            return err.messages, 400
        
        recipe = Recipe.query.get(ingredient_data.recipe_id)
        if recipe is None:
            return {"message": "Recipe could not be found for ingredient."}, 400
        
        message = "Updated existing ingredient."
        ing_name_lower = ingredient_data.name.lower()
        recipe_ing_names = [i.name.lower() for i in recipe.ingredients]
        ingredient = Ingredient.query.get(ingredient_data.id)
        if ingredient is None:
            if ing_name_lower in recipe_ing_names:
                return {"message": "Ingredient already exists in recipe."}, 400
            
            message = "Created new ingredient."
            # Create new ingredient
            ingredient = Ingredient(
                name=ingredient_data.name,
                quantity=ingredient_data.quantity,
                recipe_id=ingredient_data.recipe_id
            )
        else:
            if ingredient.name.lower() != ing_name_lower:
                # Check if trying to change to name that already exists
                if ing_name_lower in recipe_ing_names:
                    return {"message": "Ingredient already exists in recipe."}, 400
            
            # Update existing ingredient
            ingredient.name = ingredient_data.name
            ingredient.quantity = ingredient_data.quantity
            ingredient.recipe_id = ingredient_data.recipe_id
        
        try:
            db.session.add(ingredient)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable to update ingredient."}, 500

        # dump/serialize
        ingredient_result = ingredient_schema.dump(Ingredient.query.get(ingredient.id))
        return {"message": message, "ingredient": ingredient_result}

    @classmethod
    def delete_from_db(cls, _id):
        ingredient = Ingredient.query.get(_id)
        if ingredient is None:
            return {"message": "Ingredient could not be found."}, 404
        
        try:
            db.session.delete(ingredient)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable to delete ingredient."}, 500
        
        # dump/serialize
        ingredient_result = ingredient_schema.dump(ingredient)
        return {"message": "Deleted ingredient.", "ingredient": ingredient_result}
