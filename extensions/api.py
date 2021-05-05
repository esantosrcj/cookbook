from flask_restful import Api

from controllers.signup import SignupController
from controllers.login import LoginController, RefreshController, LogoutController
from controllers.recipe import RecipeController, RecipeListController
from controllers.ingredient import IngredientController, IngredientListController
from controllers.user import UserListController

api = Api()
api.add_resource(SignupController, "/signup")
api.add_resource(LoginController, "/login")
api.add_resource(LogoutController, "/logout")
api.add_resource(UserListController, "/users")
api.add_resource(RefreshController, "/refresh")
api.add_resource(RecipeListController, "/recipes")
api.add_resource(RecipeController, "/recipe", "/recipe/<int:id>")
api.add_resource(IngredientListController, "/ingredients")
api.add_resource(IngredientController, "/ingredient", "/ingredient/<int:id>")