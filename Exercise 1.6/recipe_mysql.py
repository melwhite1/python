import mysql.connector

conn = mysql.connector.connect(host='localhost', user='cf-python', passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
  choice = ""
  while(choice != "quit"):
    print("\n======================================================")
    print("\nMain Menu:")
    print("-------------")
    print("Pick a choice:")
    print("   1. Create a new recipe")
    print("   2. Search for a recipe by ingredient")
    print("   3. Update an existing recipe")
    print("   4. Delete a recipe")
    print("   5. View all recipes")
    print("\n   Type 'quit' to exit the program.")
    choice = input("\nYour choice: ")
    print("\n======================================================\n")

    if choice == "1":
      create_recipe(conn, cursor)
    elif choice == "2":
      search_recipe(conn, cursor)
    elif choice == "3":
      update_recipe(conn, cursor)
    elif choice == "4":
      delete_recipe(conn, cursor)
    elif choice == "5":
      view_all_recipes(conn, cursor)

def create_recipe(conn, cursor):
  recipe_ingredients = []
  name = str(input("\nEnter the name of the recipe: "))
  cooking_time = int(input("Enter the cooking time (minutes): "))
  ingredient = input("Enter the ingredients: ")
  recipe_ingredients.append(ingredient)
  difficulty = calc_difficulty(cooking_time, recipe_ingredients)
  recipe_ingredients_str = ", ".join(recipe_ingredients)
  sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
  val = (name, recipe_ingredients_str, cooking_time , difficulty)

  cursor.execute(sql, val)
  conn.commit()
  print("Recipe saved into the database.")

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

def search_recipe(conn, cursor):
  all_ingredients = []
  cursor.execute("SELECT ingredients FROM Recipes")
  results = cursor.fetchall()
  for recipe_ingredients_list in results:
    for recipe_ingredients in recipe_ingredients_list:
      recipe_ingredient_split = recipe_ingredients.split(", ")
      all_ingredients.extend(recipe_ingredient_split)

  all_ingredients = list(dict.fromkeys(all_ingredients))

  all_ingredients_list = list(enumerate(all_ingredients))

  print("\nAll ingredients list:")
  print("------------------------")

  for index, tup in enumerate(all_ingredients_list):
    print(str(tup[0]+1) + ". " + tup[1])

  try:
    ingredient_searched_nber = input("\nEnter the number corresponding to the ingredient you want to select from the above list: ")

    ingredient_searched_index = int(ingredient_searched_nber) - 1

    ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

    print("\nYou selected the ingredient: ", ingredient_searched)

  except:
    print("An unexpected error occurred. Make sure to select a number from the list.")

  else:
    print("\nThe recipe(s) below include(s) the selected ingredient: ")
    print("-------------------------------------------------------")

    cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ('%' + ingredient_searched + '%', ))

    results_recipes_with_ingredient = cursor.fetchall()
    for row in results_recipes_with_ingredient:
      print("\nID: ", row[0])
      print("name: ", row[1])
      print("ingredients: ", row[2])
      print("cooking_time: ", row[3])
      print("difficulty: ", row[4])

def update_recipe(conn, cursor):
  view_all_recipes(conn, cursor)
  recipe_id_for_update = int((input("\nEnter the ID of the recipe you want to update: ")))
  column_for_update = str(input("\nEnter the data you want to update among name, cooking time and ingredients: (select 'name' or 'cooking_time' or 'ingredients'): "))
  updated_value = (input("\nEnter the new value for the recipe: "))
  print("Choice: ", updated_value)

  if column_for_update == "name":
    cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (updated_value, recipe_id_for_update))
    print("Modification done.")

  elif column_for_update == "cooking_time":
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (updated_value, recipe_id_for_update))
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id_for_update, ))
    result_recipe_for_update = cursor.fetchall()

    name = result_recipe_for_update[0][1]
    recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
    cooking_time = result_recipe_for_update[0][3]

    updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
    print("Updated difficulty: ", updated_difficulty)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, recipe_id_for_update))
    print("Modification done.")

  elif column_for_update == "ingredients":
    cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (updated_value, recipe_id_for_update))
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id_for_update, ))
    result_recipe_for_update = cursor.fetchall()

    print("result_recipe_for_update: ", result_recipe_for_update)

    name = result_recipe_for_update[0][1]
    recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
    cooking_time = result_recipe_for_update[0][3]
    difficulty = result_recipe_for_update[0][4]

    updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
    print("Updated difficulty: ", updated_difficulty)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, recipe_id_for_update))
    print("Modification done.")

  conn.commit()

def delete_recipe(conn, cursor):
  view_all_recipes(conn, cursor)
  recipe_id_for_deletion = (input("\nEnter the ID of the recipe you want to delete: ")) 
  cursor.execute("DELETE FROM Recipes WHERE id = (%s)", (recipe_id_for_deletion, ))

  conn.commit()
  print("\nRecipe successfully deleted from the database.")

def view_all_recipes(conn, cursor):
  print("\nAll recipes can be found below: ")
  print("-------------------------------------------")

  cursor.execute("SELECT * FROM Recipes")
  results = cursor.fetchall()

  for row in results:
    print("\nID: ", row[0])
    print("name: ", row[1])
    print("ingredients: ", row[2])
    print("cooking_time: ", row[3])
    print("difficulty: ", row[4])

main_menu(conn, cursor)
print("Bye!\n")