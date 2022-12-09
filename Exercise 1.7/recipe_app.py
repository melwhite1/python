from sqlalchemy import create_engine
engine = create_engine("mysql://cf-python:password@localhost/my_database")

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column
from sqlalchemy.types import Integer, String

class Recipe(Base):
  __tablename__ = "final_recipes"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"

  def __str__(self):
    output = "\nName: " + str(self.name) + \
      "\nCooking time (minutes): " + str(self.cooking_time) + \
      "\nDifficulty: " + str(self.difficulty) + \
      "\nIngredients: " + str(self.ingredients)
    return output

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def calc_difficulty(cooking_time, recipe_ingredients):
  print("Run the calc_difficulty with: ", cooking_time, recipe_ingredients)

  if (cooking_time < 10) and (len(recipe_ingredients) < 4):
    difficulty_level = "Easy"
  elif (cooking_time < 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = "Medium"
  elif (cooking_time >= 10) and (len(recipe_ingredients) < 4):
    difficulty_level = "Intermediate"
  elif (cooking_time >= 10) and (len(recipe_ingredients) >= 4):
    difficulty_level = "Hard"
  else:
    print("Something bad happened, please try again")
  
  print("Difficulty level: ", difficulty_level)
  return difficulty_level

def return_ingredients_as_list():
  recipes_list = session.query(Recipe).all()
  for recipe in recipes_list:
    print("Recipe: ", recipe)
    print("recipe.ingredients: ", recipe.ingredients)
    recipe_ingredients_list = recipe.ingredients.split(", ")
    print(recipe_ingredients_list)

def create_recipe():
  recipe_ingredients = []
  name = str(input("\nEnter the name of the recipe: "))
  cooking_time = int(input("Enter the cooking time (minutes): "))
  ingredient = input("Enter the ingredients: ")
  recipe_ingredients.append(ingredient)
  recipe_ingredients_str = ", ".join(recipe_ingredients)
  print(recipe_ingredients_str)
  difficulty = calc_difficulty(int(cooking_time), recipe_ingredients)

  recipe_entry = Recipe(
    name = name,
    cooking_time = int(cooking_time),
    ingredients = recipe_ingredients_str,
    difficulty = difficulty
  )

  print(recipe_entry)

  session.add(recipe_entry)
  session.commit()

print("Recipe saved into the database.")

def view_all_recipes():
  all_recipes = []
  all_recipes = session.query(Recipe).all()

  if len(all_recipes) == 0:
    print("There is no recipe in the database")
    return None

  else:
    print("\nAll recipes can be found below: ")
    print("-------------------------------------------")

    for recipe in all_recipes:
      print(recipe)

def search_by_ingredients():
  if session.query(Recipe).count() == 0:
    print("There is no recipe in the database")
    return None

  else:
    results = session.query(Recipe.ingredients).all()
    print("results: ", results)

    all_ingredients = []

    for recipe_ingredients_list in results:
      for recipe_ingredients in recipe_ingredients_list:
        recipe_ingredient_split = recipe_ingredients.split(", ")
        all_ingredients.extend(recipe_ingredient_split)

    print("all_ingredients after the loop: ", all_ingredients)

    all_ingredients = list(dict.fromkeys(all_ingredients))

    all_ingredients_list = list(enumerate(all_ingredients))

    print("\nAll ingredients list:")
    print("------------------------")

    for index, tup in enumerate(all_ingredients_list):
      print(str(tup[0]+1) + ". " + tup[1])

    try:
      ingredient_searched_nber = input("\nEnter the number corresponding to the ingredient you want to select from the above list. You can enter several numbers. In this case, numbers shall be separated by a space: ")

      ingredients_nber_list_searched = ingredient_searched_nber.split(" ")

      ingredient_searched_list = []
      for ingredient_searched_nber in ingredients_nber_list_searched:
        ingredient_searched_index = int(ingredient_searched_nber) - 1
        ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

        ingredient_searched_list.append(ingredient_searched)

      print("\nYou selected the ingredient(s): ", ingredient_searched_list)

      conditions = []

      for ingredient in ingredient_searched_list:
        like_term = "%"+ingredient+"%"
        condition = Recipe.ingredients.like(like_term)
        conditions.append(condition)
      print("conditions: ", conditions)

      searched_recipes = session.query(Recipe).filter(*conditions).all()
      
      print(searched_recipes)

    except:
      print("An unexpected error occurred. Make sure to select a number from the list.")

    else:

      print("searched_recipes: ")
      for recipe in searched_recipes:
        print(recipe)

def delete_recipe():
  if session.query(Recipe).count() == 0:
    print("There is no recipe in the database")
    return None

  else:
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    print("results: ", results)
    print("Lits of available recipes:")
    for recipe in results:
      print("\nId: ", recipe[0])
      print("Name: ", recipe[1])

    recipe_id_for_deletion = (input("\nEnter the ID of the recipe you want to delete: "))

    recipe_to_be_deleted = session.query(Recipe).filter(Recipe.id == recipe_id_for_deletion).one()

    print("\nWARNING: You are about to delete the following recipe: ")
    print(recipe_to_be_deleted)

    deletion_confirmed = input("\nPlease confirm you want to delete the entry above (y/n): ")
    if deletion_confirmed == "y":
      session.delete(recipe_to_be_deleted)

      session.commit()
      print("\nRecipe successfully deleted from the database.")
    else:
      return None
      
def edit_recipe():
  if session.query(Recipe).count() == 0:
    print("There is no recipe in the database")
    return None

  else:
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    print("results: ", results)
    print("Lits of available recipes:")
    for recipe in results:
      print("\nId: ", recipe[0])
      print("Name: ", recipe[1])

    recipe_id_for_edit = int((input("\nEnter the ID of the recipe you want to edit: ")))

    print(session.query(Recipe).with_entities(Recipe.id).all())

    recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
    recipes_id_list = []

    for recipe_tup in recipes_id_tup_list:
      print(recipe_tup[0])
      recipes_id_list.append(recipe_tup[0])

    print(recipes_id_list)

    if recipe_id_for_edit not in recipes_id_list:
      print("Not in the ID list, please try again later.")
    else:
      print("Ok you can continue")
      recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).one()
      
      print("\nWARNING: You are about to edit the following recipe: ")
      print(recipe_to_edit)

      column_for_update = int(input("\nEnter the data you want to update among 1. name, 2. cooking time and 3. ingredients: (select '1' or '2' or '3'): "))

      updated_value = (input("\nEnter the new value for the recipe: "))
      print("Choice: ", updated_value)

      if column_for_update == 1: 
        print("You want to update the name of the recipe")
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update({Recipe.name: updated_value})
        session.commit()

      elif column_for_update == 2: 
        print("You want to update the cooking time of the recipe")
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update({Recipe.cooking_time: updated_value})
        session.commit()

      elif column_for_update == 3: 
        print("You want to update the ingredients of the recipe")
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update({Recipe.ingredients: updated_value})
        session.commit()

      else:
        print("Wrong input, please try again.")

      updated_difficulty = calc_difficulty(recipe_to_edit.cooking_time, recipe_to_edit.ingredients)
      print("updated_difficulty: ", updated_difficulty)

      recipe_to_edit.difficulty = updated_difficulty

      session.commit()
      print("Modification done.")

def main_menu():
  choice = ""
  while(choice != "quit"):
    print("\n======================================================")
    print("\nMain Menu:")
    print("-------------")
    print("Pick a choice:")
    print("   1. Create a new recipe")
    print("   2. Search for a recipe by ingredient")
    print("   3. Edit an existing recipe")
    print("   4. Delete a recipe")
    print("   5. View all recipes")
    print("\n   Type 'quit' to exit the program.")
    choice = input("\nYour choice: ")
    print("\n======================================================\n")

    if choice == "1":
      create_recipe()
    elif choice == "2":
      search_by_ingredients()
    elif choice == "3":
      edit_recipe()
    elif choice == "4":
      delete_recipe()
    elif choice == "5":
      view_all_recipes()
    else:
      if choice == "quit":
        print("Bye!\n")
      else:
        print("WARNING... Wrong entry, please try again.")

main_menu()

session.close()