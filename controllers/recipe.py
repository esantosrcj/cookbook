from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.recipe import RecipeService

# Similar to a Controller class in Java
class RecipeController(Resource):

    @jwt_required()
    def get(self, id):
        return RecipeService.find_by_id(_id=id)

    @jwt_required(fresh=True)
    def post(self):
        json_data = request.get_json()
        # EMPTY sequences are False
        if not json_data:
            return {"message": "No input data provided."}, 400
        
        service = RecipeService(data=json_data)
        return service.save_to_db()
    
    @jwt_required(fresh=True)
    def put(self):
        json_data = request.get_json()
        # EMPTY sequences are False
        if not json_data:
            return {"message": "No input data provided."}, 400
        
        service = RecipeService(data=json_data)
        return service.update_in_db()
    
    @jwt_required(fresh=True)
    def delete(self, id):
        return RecipeService.delete_from_db(_id=id)


class RecipeListController(Resource):

    # jwt_required is optional; endpoint can accessed without JWT but limited data is returned
    @jwt_required(optional=True)
    def get(self):
        recipes = RecipeService.find_all()
        user_id = get_jwt_identity()
        if user_id:
            return recipes, 200
        else:
            recipe_names = [r["name"] for r in recipes]
            return {"recipes": recipe_names, "message": "More data available if you log in."}
