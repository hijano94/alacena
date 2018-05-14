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
NUM=5 		# Número de recetas solicitadas a la API
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
			dic["calorias"]=int(re["recipe"]["calories"])
			dic["ingredientes"]=re["recipe"]["ingredientLines"]
			dic["coin"]=0
			dic["listcoin"]=[]
			if 'Vegan' in re["recipe"]["healthLabels"]:	
				dic["vegan"]=True
			else:
				dic["vegan"]=False	
			RECETAS.append(dic)
	else:
		print("\n####################### API no disponible... ################################\n")

def	Coincidencias (ingre):
	for receta in RECETAS:
		for ing in ingre.strip().split(","):
			for x in receta["ingredientes"]:
				if ing.upper() in x.upper():
					receta["coin"]+=1
					receta["listcoin"].append(ing)
					break

def ImprimirConsola (datos):
	print("######## RECETAS ########")
	for receta in datos:
		print("\n    @ %s"%receta["nombre"])
		print("        > Imagen: %s"%receta["imagen"])
		print("        > Url: %s"%receta["url"])
		print("        > Calorias: %f kcal"%receta["calorias"])
		print("        > Vegano:",receta["vegan"])
		print("        > Coincidencias: %i"%receta["coin"])
		print("        > ",receta["listcoin"])
		print("        > Ingredientes:")
		for ing in receta["ingredientes"]:
			print("            * %s"%ing)

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
		RECETAS.clear()
		params={}
		params["ingredientes"] = request.form['ingredientes'] 
		if request.form["menos"] == "True" and request.form["calorias"] != '' :
			params["calorias"]= "lte %s"%request.form["calorias"]
		elif request.form["menos"] == "False" and request.form["calorias"] != '':  
			params["calorias"]= "gte %s"%request.form["calorias"]
		else:
			params["calorias"]= None
		if request.form['salud'] == "None" or request.form['salud'] == "on":
			params["salud"]=None
		else:	
			params["salud"]= request.form['salud']
		print(request.form['dieta'])	
		if request.form['dieta'] == "None" or request.form['dieta'] == "on":
			params["dieta"]=None
		else:	
			params["dieta"]= request.form['dieta']

		for ing in params["ingredientes"].strip().split(","):
			HEAD = {
			'app_id':os.environ["recipe_id"],
			'app_key': os.environ["recipe_key"], 
			'q' : ing,
			'calories' : params["calorias"],
			'to' : NUM,
			'diet': params["dieta"],
			'health': params["salud"]
			}
			print(HEAD)
			SolicitarRecetas(ing,HEAD)
		
		Coincidencias(params["ingredientes"])
		RECETAS.sort(key=lambda x: x["coin"], reverse=True)

		return redirect("/resultados/0")

@app.route('/resultados/<ini>')
def Resultados(ini):
	datos=[]
	for idx,x in enumerate(RECETAS):
		if idx < PAG:
			datos.append(x)
		else:
			break	

	ImprimirConsola(datos)
	return render_template("resultados.html", datos = datos)

@app.route('/despensa')
def Despensa():
	if request.method=="GET":
		return render_template("search.html",datos=None)
	#else:	




if __name__ == '__main__':
	port=os.environ["PORT"]
	app.run('0.0.0.0',int(port), debug=True)