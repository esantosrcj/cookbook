from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.ingredient import IngredientService

# Similar to a Controller class in Java
class IngredientController(Resource):

    @jwt_required()
    def get(self, id):
        return IngredientService.find_by_id(_id=id)
    
    # Only allow fresh JWTs to access this endpoint with the "fresh=True" argument
    @jwt_required(fresh=True)
    def post(self):
        json_data = request.get_json()
        # EMPTY sequences are False
        if not json_data:
            return {"message": "No input data provided."}, 400
        
        service = IngredientService(data=json_data)
        return service.save_to_db()

    @jwt_required(fresh=True)
    def put(self):
        json_data = request.get_json()
        # EMPTY sequences are False
        if not json_data:
            return {"message": "No input data provided."}, 400
        
        service = IngredientService(data=json_data)
        return service.update_in_db()

    @jwt_required(fresh=True)
    def delete(self, id):
        return IngredientService.delete_from_db(_id=id)


class IngredientListController(Resource):

    # jwt_required is optional; endpoint can accessed without JWT but limited data is returned
    @jwt_required(optional=True)
    def get(self):
        ingredients = IngredientService.find_all()
        user_id = get_jwt_identity()
        if user_id:
            return ingredients, 200
        else:
            return {"ingredients": [i["name"] for i in ingredients], "message": "More data available if you log in."}
        
