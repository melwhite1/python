import pickle

def display_recipe(recipe):
  print("\nRecipe: ", recipe["name"])
  print("Cooking Time (minutes): ", recipe["cooking_time"])
  print("Ingredients: ")
  for ele in recipe["recipe_ingredients"]:
    print(ele)
  print("Difficulty level: ", recipe["difficulty"])

def search_ingredient(data):
  all_ingredients_list = list(enumerate(data["all_ingredients"]))
  
  for index, tup in enumerate(all_ingredients_list):
    print(str(tup[0]+1) + ". " + tup[1])

  try:
    ingredient_searched_nber = input("Enter the number corresponding to the ingredient you want to select from the above list: ")

    ingredient_searched_index = int(ingredient_searched_nber) - 1

    ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

    print("\nYou selected the ingredient: ", ingredient_searched)

  except:
    print("An unexpected error occurred. Make sure to select a number from the list.")

  else:
    for recipe in data["recipes_list"]:
      for recipe_ing in recipe["recipe_ingredients"]:
        if (recipe_ing == ingredient_searched):
          print("\nThe following recipe includes the searched ingredient:")
          print("------------------------------------------------------")
          display_recipe(recipe)

recipe_file_name = input("Enter the name of the file that contains your recipe data (including the .bin extension): ")

try: 
  user_recipe_file = open(recipe_file_name, "rb")
  data = pickle.load(user_recipe_file)

except FileNotFoundError:
  print("File doesn't exist - exiting.")

else:
  search_ingredient(data)
  user_recipe_file.close()