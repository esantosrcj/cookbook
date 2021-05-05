from extensions.db import db

# Combination of model/entity and repository in Java
class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # lazy:'joined'/False - load the relationship in the same query as the parent using a JOIN statement
    # Set uselist=False for one-to-one relationship
    ingredients = db.relationship(
        "Ingredient",
        backref=db.backref("recipes", lazy="joined", innerjoin=True),
        cascade="all, delete",
        passive_deletes=True
    )
