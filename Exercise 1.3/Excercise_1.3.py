import pdb
recipes_list = []
ingredients_list = []

n = int(input("How many recipes would you like to enter?: "))

def take_recipe(name="No name", cooking_time="No cooking time", ingredients="no ingredients", difficulty="no diffculty", recipe="no recipe"):
  name = input("Enter the name of your recipe: ")
  cooking_time = int(input("Enter the cooking time for your recipe in minutes: "))
  ingredients = input("Enter the ingredients for your recipe: ")
  recipe = {
    'Name' : name,
    'Cooking_Time' : cooking_time,
    'Ingredients' : ingredients.split(', '),
    'Difficulty' : difficulty
  }
  return recipe  

for x in range(n):
  recipe = take_recipe()
  for ingredient in recipe['Ingredients']:
    if ingredient not in ingredients_list:
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

for recipe in recipes_list:
  if int(recipe['Cooking_Time']) < 10 and len(recipe['Ingredients']) < 4:
    difficulty = 'Easy' 
  elif int(recipe['Cooking_Time']) < 10 and len(recipe['Ingredients']) >= 4:
    difficulty = 'Medium'
  elif int(recipe['Cooking_Time']) >= 10 and len(recipe['Ingredients']) < 4:
    difficulty = 'Intermediate'
  elif int(recipe['Cooking_Time']) >= 10 and len(recipe['Ingredients']) >= 4:
    difficulty = 'Hard'

  print('==================================================')
  print('Recipe: ', recipe['Name'])
  print('Cooking Time (min): ', recipe['Cooking_Time'])
  print('Ingredients: ' )
  for ingredient in recipe['Ingredients']:
      print(ingredient)
  print('Difficulty level: ', difficulty)    


print('''Ingredients available across all recipes
-------------------------------------------- ''')     
ingredients_list = []
for recipe in recipes_list:
    for ingredient in recipe['Ingredients']:
        ingredients_list.append(ingredient)
for i in ingredients_list:
    print(i)
