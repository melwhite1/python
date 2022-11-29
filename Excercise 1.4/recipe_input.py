import pickle

recipes_list = []
ingredients_list = []

def take_recipe():
  name = str(input("\nName of the recipe: "))
  cooking_time = int(input("Cooking time (minutes): "))
  ingredients = input("Enter the ingredients for your recipe: ")
  difficulty = calc_difficulty(cooking_time, ingredients)
  recipe = {
    "name": name,
    "cooking_time": cooking_time,
    "recipe_ingredients": ingredients.split(', '),
    "difficulty": difficulty,
  }

  return recipe


def calc_difficulty(cooking_time, ingredients):
  print("Run the calc_difficulty with: ", cooking_time, ingredients)

  if (cooking_time < 10) and (len(ingredients) < 4):
    difficulty_level = "Easy"
  elif (cooking_time < 10) and (len(ingredients) >= 4):
    difficulty_level = "Medium"
  elif (cooking_time >= 10) and (len(ingredients) < 4):
    difficulty_level = "Intermediate"
  elif (cooking_time >= 10) and (len(ingredients) >= 4):
     difficulty_level = "Hard"
  else:
    print("Something bad happened, please try again")
  
  print("Difficulty level: ", difficulty_level)
  return difficulty_level


try:
  recipe_file_name = input("Enter the name of the file that contains your recipe data (including the .bin extension): ")
  my_recipes_file = open(recipe_file_name, 'rb')
  data = pickle.load(my_recipes_file)

except FileNotFoundError:
  print("File doesn't exist - exiting.")
  data = {
    "recipes_list": [],
    "all_ingredients": [],
  }

except:
  print("An unexpected error occurred.")
  data = {
    "recipes_list": [],
    "all_ingredients": [],
  }

else:
  my_recipes_file.close()

finally:
  recipes_list = data["recipes_list"]
  ingredients_list = data["all_ingredients"]
  print("Data from finally: ", data)
  print("Recipes list from finally: ", recipes_list)
  print("Ingredient list from finally: ", ingredients_list)

  n = int(input("Please specify how many recipes you want to enter: "))

  for n in range(0,n):
    recipe = take_recipe()
    print("Recipe dictionary: ", recipe)
    recipes_list.append(recipe)

    print("\nRecipe: ", recipe["name"])

    print("Cooking Time (min): ", recipe["cooking_time"])

    print("Ingredients: ")
    for ele in recipe["recipe_ingredients"]:
      print(ele)
      if ele in ingredients_list:
        continue
      else:
        ingredients_list.append(ele)

    calc_difficulty(recipe["cooking_time"], recipe["recipe_ingredients"])

  ingredients_list.sort()

  print("\n\nIngredients Available Accross All Recipies: ")
  print("--------------------------------------------")
  for ingredient in ingredients_list:
    print(ingredient)

  data = {
    "recipes_list": recipes_list,
    "all_ingredients": ingredients_list,
  }

  print("Data from the data variable: ", data)

  my_recipes_file = open(recipe_file_name, 'wb')
  pickle.dump(data, my_recipes_file)
  my_recipes_file.close()