# Capstone Project Proposal  
Dru Serkes

---

### The Pitch  
Do you enjoy discovering and trying out new recipes? 
Do you get exasperated cobbling together shopping lists?
Are you just looking for recipes that fit your diet? 
Whether you eat Vegan, Whole30, or whatever ends up on your plate, you are certain to find recipes to satisfy your appetite with “The Easy Meal ” (working title). 
Search for recommendations for recipes based on your personal criteria, and save your favorites. 
Select which meals you want to try out, and we’ll build a shopping list for you (no headache). 
Then when you’re ready, you can email your shopping list to yourself so you know exactly what to get the next time you go out!

---

### The Goal, The User  

For my first capstone project, I would like to create a website that assists users in their search for exciting new meals. 
Over the past 3 months, I’ve watched my partner search online for hours for recipes to make for dinner for 7-10 days at a time, then watched her scribble down a grocery list to take food shopping. 
Further complicating things, sometimes we like to adhere to certain types of diets (we’ve done 7 Whole30’s), reducing our options for what to make. 
I would like my project to assist in this process by allowing users (like her) to find recipes based on their needs, save their favorites, then have their grocery lists made for them. 
We live in a world where our time is increasingly limited and valuable. Our target user is someone who both understands this, and has a passion for cooking new dishes, either as a hobbyist or full-fledged homemaker.

---

### The Data  

Currently, I plan to utilize the [Spoonacular api](https://spoonacular.com/food-api) for data. I intend to make extensive use of their endpoints to: search recipes, get recipe information (including ingredients), and get analyzed recipe instructions.

---

### The Approach  

The database schema for this project will include a table for users with a name, email, password (hashed for security), and optional fields for diet (string) and a list for intolerances (as strings) that can be added via the user profile. 
There will also be a table for any saved recipes. This table will include the recipe ID (use API ID), the recipe title, description, image url, source url, ready_in, and servings. 
These two tables will be connected via a many-to-many relationship. 
A third table will be for ingredients, with an id (use API ID), name, amount and unit of measurement.
The ingredients and recipes tables will be connected via a many-to-many relationship; there will also be a grocery list table connecting users with ingredients. 
A fourth table will be for steps. Each step will have a recipe id foreign key (for its corresponding recipe), a number (step: 1, 2, 3…) and step (string for instructions). 
All of this stated, I think the largest initial hurdle will be navigating logic for saving recipe information to the database. This is the most many-to-many relationships I’ve worked with, and I’ll have to check my db for recipes to see if it has been saved already by another user before saving any new recipe information as this will be an extensive process, and each recipe will contain ingredients and steps that also need to be checked for and saved separately. 
The API itself presents the issue of a free API key only permitting a limited number of calls per day. To help with this, I have applied for a student API key, in hopes of adding flexibility while in development. 

---

### User Flow  

User will create an account / log in. The main interface will have a search (list of results initially populated with random recipes). The search will include options to refine the search (checkboxes for cuisines or intolerances) as well as search recipes that are like user input. 
Each list item from the results will be represented by a card consisting of the recipe title, image, “ready in” time and the amount of servings. Each card will include a button with a heart image (or something similar) that, when clicked, adds/removes the recipe from the users’ favorites. 
Short logic digression: adding a recipe to favorites will check the recipes table for that recipe id (PK - indexed). If found, it can simply add the user and recipe id’s to the users_recipes table. Otherwise, it will populate the db with all of the necessary data for that recipe. Removing a recipe from favorites will simply remove the user and recipe relationship, but keep the recipe in the db to limit future API calls.
There will be a link in the nav for the user to view their favorites, which will initially be displayed as a list of cards (much like the search). Clicking on a card will navigate the user to a page where the user can view the recipe information (description, ingredients, steps, etc).
The recipe detail page will include a button to add the recipes’ ingredients to a users’ grocery list. When clicked, it will automatically populate this list (aka the grocery_list table). 
The users’ grocery list can be viewed by clicking its corresponding link in the nav. On this page, a user will have the option to remove ingredients from their list individually, to clear their list entirely, and to email this list to themselves.

---

### Stretch goals  

As this is my first project where I define the expectations, I feel this is a sizable amount of work to ask of myself to start. I believe this product can be useful as I currently imagine it. 
If I end up with extra time and want to add more functionality, I would love to dig into how the user may further refine their search. It would also be fun to allow the user to email their shopping list to a friend, rather than themselves, and to share meals in general. 
I would also love to add functionality for a user to be able to decide whether recipes display measurements in US or metric units.  

