import requests
import json
import os

#### VARIABLES GLOBALES ####
URL="https://test-es.edamam.com/search"
RECETAS=[]
NUM=20 		# Número de recetas solicitadas a la API
PAG=10		# Número de recetas por página

#### FUNCIONES ####

def SolicitarRecetas (ingrediente):
	HEAD = {
		'app_id':os.environ["recipe_id"],
		'app_key': os.environ["recipe_key"], 
		'q' : ingrediente,
		'to' : NUM
		}
	c=requests.get(URL ,params=HEAD)
	
	if c.status_code == 200:
		todo=c.json()
		for re in todo["hits"]:
			dic={}
			dic["nombre"]=re["recipe"]["label"]
			dic["imagen"]=re["recipe"]["image"]
			dic["url"]=re["recipe"]["url"]
			dic["calorias"]=re["recipe"]["calories"]
			dic["ingredientes"]=re["recipe"]["ingredientLines"]
			dic["coin"]=0
			if 'Vegan' in re["recipe"]["healthLabels"]:	
				dic["vegan"]=True
			else:
				dic["vegan"]=False	
			RECETAS.append(dic)
	else:
		print("API no disponible...")

def	Coincidencias (ingre):
	for receta in RECETAS:
		for ing in ingre.strip().split(","):
			for x in receta["ingredientes"]:
				if ing.upper() in x.upper():
					receta["coin"]+=1			

def ImprimirConsola ():
	print("######## RECETAS ########")
	for receta in RECETAS:
		print("\n    @ %s"%receta["nombre"])
		print("        > Imagen: %s"%receta["imagen"])
		print("        > Url: %s"%receta["url"])
		print("        > Calorias: %f kcal"%receta["calorias"])
		print("        > Vegano:",receta["vegan"])
		print("        > Coincidencias: %i"%receta["coin"])
		print("        > Ingredientes:")
		for ing in receta["ingredientes"]:
			print("            * %s"%ing)

############ MAIN ##############

ingredientes=input("Introduce los ingredientes separados por comas: ")
for ing in ingredientes.strip().split(","):
	SolicitarRecetas(ing)
	Coincidencias(ingredientes)
sorted(RECETAS,key=lambda x: x["coin"])
ImprimirConsola()