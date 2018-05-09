import requests
import json
import os

#### VARIABLES GLOBALES ####
URL="https://test-es.edamam.com/search"


#### FUNCIONES ####
ingrediente=input("Introduce el ingrediente: ")
HEAD = {'app_id':os.environ["recipe_id"],'app_key': os.environ["recipe_key"], 'q' : ingrediente}
c=requests.get(URL ,params=HEAD)

if c.status_code == 200:
	recetas=c.json()
	print("Numero de recetas encontradas: %i"%recetas["count"])
	print("From: %i"%recetas["from"])
	print("To: %i"%recetas["to"])
	print("Params: %s"%recetas["params"])
	print("######## RECETAS ########")
	for receta in recetas["hits"]:
		print("\n    @ %s"%receta["recipe"]["label"])
		print("        > Imagen: %s"%receta["recipe"]["image"])
		print("        > Url: %s"%receta["recipe"]["url"])
		print("        > Calorias: %f kcal"%receta["recipe"]["calories"])
		print("        > Ingredientes:")
		for ing in receta["recipe"]["ingredientLines"]:
			print("            * %s"%ing)
		print("        > Etiquetas:")	
		for eti in receta["recipe"]["healthLabels"]:
			print("            * %s"%eti)
else:
	print("API no disponible...")	
