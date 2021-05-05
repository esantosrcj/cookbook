from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from extensions.db import db
from models.recipe import Recipe
from schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

class RecipeService:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"<RecipeService >"

    @classmethod
    def find_all(cls):
        recipes = Recipe.query.order_by(Recipe.id.asc()).all()
        # dump/serialize
        recipes_result = recipes_schema.dump(recipes)
        return recipes_result
    
    @classmethod
    def find_by_id(cls, _id):
        recipe = Recipe.query.get(_id)
        if recipe:
            # dump/serialize
            recipe_result = recipe_schema.dump(recipe)
            return recipe_result
        
        return {"message": "Recipe could not be found."}, 404
    
    @classmethod
    def find_by_name(cls, name):
        return Recipe.query.filter_by(name=name).first()
    
    def save_to_db(self):
        # Validate and deserialize
        try:
            # TODO: Convert to Recipe object???
            # load/deserialize to OrderedDict
            data = recipe_schema.load(self.data)
        except ValidationError as err:
            return err.messages, 400

        recipe_name = data["name"]
        recipe_names = [recipe.name.lower() for recipe in Recipe.query.all()]
        if recipe_name.lower() in recipe_names:
            return {"message": "Recipe already exists."}, 400
        
        ingredients = data["ingredients"]
        recipe = Recipe(name=recipe_name, ingredients=ingredients)

        try:
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable to add recipe."}, 500
        
        # dump/serialize
        recipe_result = recipe_schema.dump(Recipe.query.get(recipe.id))
        return {"message": "Created new recipe.", "recipe": recipe_result}
    
    def update_in_db(self):
        # Validate and deserialize
        try:
            # TODO: Convert to Recipe object???
            # load/deserialize to OrderedDict
            data = recipe_schema.load(self.data)
        except ValidationError as err:
            return err.messages, 400
        
        message = "Updated existing recipe."
        recipe_name = data["name"]
        ingredients = data["ingredients"]
        recipe_names = [recipe.name.lower() for recipe in Recipe.query.all()]
        recipe = Recipe.query.get(data["id"])
        if recipe:
            if recipe_name.lower() != recipe.name.lower():
                # Check if trying to change to name that already exists
                if recipe_name.lower() in recipe_names:
                    return {"message": "Recipe already exists."}, 400
            
            # Update existing recipe
            recipe.name = recipe_name
            # TODO: Check for existing ingredients and update them with the new values
            # append(): adds an element at the end of the list
            # extend(): add the elements of a list to the end of the current list
            recipe.ingredients.extend(ingredients)
        else:
            if recipe_name.lower() in recipe_names:
                return {"message": "Recipe already exists."}, 400
            
            message = "Created new recipe."
            # Create new recipe
            recipe = Recipe(name=recipe_name, ingredients=ingredients)
        
        try:
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable to update recipe."}, 500

        # dump/serialize
        recipe_result = recipe_schema.dump(Recipe.query.get(recipe.id))
        return {"message": message, "recipe": recipe_result}

    @classmethod
    def delete_from_db(self, _id):
        recipe = Recipe.query.get(_id)
        if recipe is None:
            return {"message": "Recipe could not be found."}, 404
        
        try:
            for ingredient in recipe.ingredients:
                db.session.delete(ingredient)
            db.session.delete(recipe)
            db.session.commit()
        except SQLAlchemyError:
            return {"message": "Unable to delete recipe."}, 500
        
        # dump/serialize
        recipe_result = recipe_schema.dump(recipe)
        return {"message": "Deleted recipe.", "recipe": recipe_result}
