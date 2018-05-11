from flask import Flask
from flask import render_template,request,redirect,session
import requests
import json
import os
app = Flask(__name__)

##########################################
#         VARIABLES GLOBALES             #
##########################################

URL="https://test-es.edamam.com/search"
RECETAS=[]
NUM=20 		# Número de recetas solicitadas a la API
PAG=10		# Número de recetas por página

##########################################
#              FUNCIONES                 #
##########################################

def SolicitarRecetas (ingrediente,HEAD):
	
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

###########################################
#                 MAIN                    #
###########################################

@app.route('/')
def Inicio():
	return render_template("index.html")

@app.route('/buscar', methods=['GET', 'POST'])
def Buscar():
	if request.method=="GET":
		return render_template("search.html",datos=None)
	else:
		params={}
		params["ingredientes"] = request.form['ingredientes']   
		print(params["ingredientes"])
		
		for ing in params["ingredientes"].strip().split(","):
			HEAD = {
			'app_id':os.environ["recipe_id"],
			'app_key': os.environ["recipe_key"], 
			'q' : ing,
			'to' : NUM
			}
			SolicitarRecetas(ing,HEAD)
			Coincidencias(params["ingredientes"])
		
		RECETAS.sort(key=lambda x: x["coin"])

		return redirect("/resultados/0")

@app.route('/resultados/<ini>')
def Resultados(ini):
	datos=[]
	for x in range(0,9):

		datos.append(RECETAS[x])
	return render_template("resultados.html", datos = datos)

#@app.route('/despensa')
#def Despensa():
	

if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0')