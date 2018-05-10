import requests
import json
import os

#### VARIABLES GLOBALES ####
URL="https://test-es.edamam.com/search"


#### FUNCIONES ####

def SolicitarRecetas (ingrediente):
	HEAD = {
		'app_id':os.environ["recipe_id"],
		'app_key': os.environ["recipe_key"], 
		'q' : ingrediente,
		'to' : 2
		}
	c=requests.get(URL ,params=HEAD)
	recetas=[]
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
			recetas.append(dic)
		return recetas		
	else:
		print("API no disponible...")


#def	Coincidencias (recetas,ingredientes):
#	for receta in recetas:
#		for ing in ingredientes:
#			if ing in receta["ingredientes"]:
#				receta[""]



#def Enviar ():



# sorted(fijos,key=lambda x: x[4])

def ImprimirConsola (recetas):
	for receta in recetas:
		print("\n    @ %s"%receta["nombre"])
		print("        > Imagen: %s"%receta["imagen"])
		print("        > Url: %s"%receta["url"])
		print("        > Calorias: %f kcal"%receta["calorias"])
		print("        > Vegano:",receta["vegan"])
		print("        > Ingredientes:")
		for ing in receta["ingredientes"]:
			print("            * %s"%ing)


ingredientes=input("Introduce los ingredientes separados por comas: ")
print("######## RECETAS ########")
for ing in ingredientes.strip().split(","):
	recetas=SolicitarRecetas(ing)
	ImprimirConsola(recetas)