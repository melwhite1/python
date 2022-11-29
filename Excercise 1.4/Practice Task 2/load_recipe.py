import pickle

with open('recipe_binary.bin', 'rb') as my_file:
  recipe = pickle.load(my_file)

print("\nRecipe details:")
print("---------------")
print("Name:  " + recipe['name'])
print("Ingredients:  ")
for ingredient in recipe['ingredients']:
  print("- " + ingredient)
print("Cooking Time:  " + str(recipe['cooking_time']))
print("Difficulty: " + recipe['difficulty'])