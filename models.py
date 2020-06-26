""" SQLAlchemy Models for Easy Meal """

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """ Connect to Database """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Model """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    img_url = db.Column(
        db.String, default='/static/images/icons8-kawaii-cupcake-64.png')
    is_admin = db.Column(db.Boolean, default=False)
    recipes = db.relationship(
        'Recipe', secondary="users_recipes", backref='users')
    grocery_lists = db.relationship('GroceryList', backref='user')

    @classmethod
    def signup(cls, data):
        """ Generate hashed password and register a new user """
        hashed = bcrypt.generate_password_hash(data['password'])
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=data['username'], password=hashed_utf8, email=data['email'], img_url=data['img_url'])

    @classmethod
    def authenticate(cls, data):
        """ Validate user exists & pwd is correct

        return user if valid; else return False
        """

        u = User.query.filter_by(username=data['username']).first()
        if u and bcrypt.check_password_hash(u.password, data['password']):
            return u
        else:
            return False

    def __repr__(self):
        return f'<User: {self.username}>'


class UserRecipe(db.Model):
    """ Many to Many Users to Recipes """
    __tablename__ = "users_recipes"

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id'), primary_key=True)


class Recipe(db.Model):
    """ Recipe Model """
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    source_url = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    ready_in = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    ingredients = db.relationship(
        "Ingredient", secondary="measurements", backref="recipes")
    steps = db.relationship("Step", backref='recipe')

    def __repr__(self):
        return f'<Recipe: {self.title}>'


class Measurement(db.Model):
    """ Many to Many Recipes to Ingredients """
    __tablename__ = "measurements"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredients.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id'))
    amount = db.Column(db.Float)
    unit = db.Column(db.String)
    recipe = db.relationship('Recipe', backref='measurements')
    ingredient = db.relationship("Ingredient", backref='measurements')

    def show_measurement(self):
        """ Returns a string with the full measurement """
        return f"{self.amount} {self.unit} {self.ingredient.name}"
    


class Ingredient(db.Model):
    """ Ingredient Model """
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Ingredient: {self.name}>'


class Step(db.Model):
    """ Step Model """

    __tablename__ = 'steps'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id'))
    number = db.Column(db.Integer)
    step = db.Column(db.String)

    def __repr__(self):
        return f'<Step: {self.number} - {self.step}>'
    
    def show_step(self):
        """ returns a string of the step number and instructions """
        return f"{self.number}. {self.step}"



class GroceryList(db.Model):
    """ Grocery List model """
    __tablename__ = 'grocery_lists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.date(datetime.now())
    )
    ingredients = db.relationship(
        'Ingredient', secondary='lists_ingredients', backref="grocery_lists")

    def __repr__(self):
        return f'<Grocery List: {self.title} for {self.user.username}>'


class ListIngredient(db.Model):
    """ Many to Many Lists to Ingredients """
    __tablename__ = "lists_ingredients"

    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredients.id'), primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'grocery_lists.id'), primary_key=True)