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
  if int(recipe['Cooking_Time']) < 10:
    if len(recipe['Ingredients']) < 4:
      difficulty = 'Easy' 
  if int(recipe['Cooking_Time']) < 10:
    if len(recipe['Ingredients']) >= 4:
      difficulty = 'Medium'
  if int(recipe['Cooking_Time']) >= 10:
    if len(recipe['Ingredients']) < 4:
      difficulty = 'Intermediate'
  if int(recipe['Cooking_Time']) >= 10:
    if len(recipe['Ingredients']) >= 4:
      difficulty = 'Hard'
  recipe['Difficulty'] = difficulty
  recipes_list.append(recipe)
