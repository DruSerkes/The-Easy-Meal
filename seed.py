""" Seed file to make sample data for pets db """

from models import User, Recipe, Measurement, Ingredient, Step, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Empty all tables
User.query.delete()
Recipe.query.delete()
Measurement.query.delete()
Ingredient.query.delete()


# Add Users
john = User(username='john', email='test@test.com', password='password')
phil = User(username='phil', email='test2@test.com', password='password')
will = User(username='will', email='test3@test.com', password='password')
darby_data = {
        'username': 'darby',
        'password': 'doggo',
        'email': 'druserkes@gmail.com',
        'img_url': User.img_url.default.arg
    }
darby = User.signup(darby_data)

# Add new objects to session, so they'll persist
db.session.add_all([john, phil, will, darby])


# Add Recipe 
cookies = Recipe(title="chocolate chip cookies", img_url="https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fimages.media-allrecipes.com%2Fuserphotos%2F4540234.jpg&w=595&h=398&c=sc&poi=face&q=85", source_name="All-Recipes", source_url="https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/", description="Warm, gooey chocolate chip cookies - so savory so yummy - you can't resist. Warm and comfy and all that good stuff", ready_in=25, servings=12) 
db.session.add(cookies)


# Add Ingredient
spray = Ingredient(name='Non-stick PAM spray')
dough = Ingredient(name='cookie dough')
db.session.add_all([spray, dough])

# Commit to db!
db.session.commit()


# Add Measurement
m1 = Measurement(recipe=cookies, ingredient=dough, amount=24, unit="spoonfuls")
db.session.add(m1)
db.session.commit()

# Add steps for recipe
s1 = Step(recipe=cookies, number=1, step="preheat oven to 350F")     
s2 = Step(recipe=cookies, number=2, step="Spray baking sheet with non-stick spray")                                                                                                                   
s3 = Step(recipe=cookies, number=3, step="Place balls of dough on baking sheet 2 inches apart")                                                                                         
s4 = Step(recipe=cookies, number=4, step="Place baking sheet in oven 10-12 minutes or until edges are light golden brown")                                                              
s5 = Step(recipe=cookies, number=5, step="Remove cookies from oven and let cool for 5 minutes")                                                                                         
s6 = Step(recipe=cookies, number=6, step="Enjoy!")
db.session.add_all([s1, s2, s3, s4, s5, s6])                                                                                                                                                
db.session.commit()  


# Add cookies recipe to user Darby 
darby.recipes.append(cookies)
db.session.commit()