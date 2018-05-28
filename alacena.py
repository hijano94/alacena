from flask import Flask
from flask import render_template,request,redirect,session
import requests
import json
import os
app = Flask(__name__)
app.secret_key = "aGiieedSLenAGdonsyyTSRD238nEA"

##########################################
#         VARIABLES GLOBALES             #
##########################################

URL="https://test-es.edamam.com/search"
URLY="https://www.googleapis.com/youtube/v3/search"
RECETAS=[]
NUM= os.environ["NUM"]		# Número de recetas solicitadas a la API
PAG=10		# Número de recetas por página

##########################################
#              FUNCIONES                 #
##########################################

def SolicitarRecetas (HEAD):
	
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
		for ing in ingre:
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
		print("        > Video:",receta["video"])
		print("        > Ingredientes:")
		for ing in receta["ingredientes"]:
			print("            * %s"%ing)

def DarIngredientes():
	with open ("usuarios/%s.json"%session["usuario"], "r+") as datos:
		usuario=json.load(datos)
		return usuario["ingredientes"]

def AnadirIng(ingrediente):
	with open ("usuarios/%s.json"%session["usuario"], "r+") as datos:
		usuario=json.load(datos)
		usuario["ingredientes"].append(ingrediente)

	with open ("usuarios/%s.json"%session["usuario"], "w") as datos:
		json.dump(usuario,datos)
	
def PedirVideo(q):

	par={
	'key': os.environ["youtube_key"],
	'part': "id",
	'q': q,
	'regionCode': "es",
	'type': "video",
	'maxResult': 1
	}

	c=requests.get(URLY ,params=par)
	print(c.status_code)
	if c.status_code == 200:
		video=c.json()
		print(video)

		return "https://www.youtube.com/watch?v="+video["items"][0]["id"]["videoId"]		
	else:
		print("\n####################### youtube no esta") 

###########################################
#                 MAIN                    #
###########################################

@app.route('/', methods=['GET', 'POST'])
def Inicio():
	if request.method=="GET":
		return render_template("index.html", error=None)
	else:
		if request.form["submit"]=="iniciar":
			try:
				with open ("usuarios/%s.json"%request.form["name"], "r+") as datos:
					usuario=json.load(datos)
					if request.form["pswd"] == usuario["pswd"]:
						session["usuario"]=usuario["nombre"]
						return redirect("/")
			except:	
				return render_template("index.html",datos=None, error="El usuario no existe")		

		elif request.form["submit"]=="registrar":
				try:
					with open ("usuarios/%s.json"%request.form["name"], "r+") as datos:
						usuario=json.load(datos)
						if usuario["nombre"]==request.form["name"]:
							return render_template("index.html",datos=None, error="Usuario ya registrado")
				except:	
					with open ("usuarios/%s.json"%request.form["name"], "w+") as datos:	
						usuario={"nombre": request.form["name"], "pswd": request.form["pswd"], "ingredientes": []}	
						json.dump(usuario,datos)
						session["usuario"]=request.form["name"]
						return render_template("index.html", datos=session)
@app.route('/salir')
def Salir():
	session.clear()
	return redirect('/')

@app.route('/buscar', methods=['GET', 'POST'])
def Buscar():
	if request.method=="GET":
		return render_template("search.html",datos=None)
	else:
		RECETAS.clear()
		params={}
		Ingredientes=[]
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
			Ingredientes.append(ing)
			SolicitarRecetas(HEAD)
		
		if "usuario" in session:
			for i in DarIngredientes():
				Ingredientes.append(i)
		Coincidencias(Ingredientes)
		RECETAS.sort(key=lambda x: x["coin"], reverse=True)
		
		return redirect("/resultados/1")

@app.route('/resultados/<int:ini>')
def Resultados(ini):
	datos=[]
	inicio=(PAG * ini)-PAG
	fin=PAG * ini
	for idx,x in enumerate(RECETAS):
		if idx >= inicio and idx < fin:
			x["video"]=PedirVideo(x["nombre"])
			datos.append(x)
		
	if ini >1:
		ant=ini-1
	else:
		ant=1
	sig=ini+1				

	Datos=[datos,ant,sig]		
	ImprimirConsola(datos)
	return render_template("resultados.html", datos = Datos)

@app.route('/despensa',methods=['GET', 'POST'])
def Despensa():
	if request.method=="GET":
		if not "usuario" in session:
			return redirect("/#popup")
		else:
			ingredientes=DarIngredientes()
			return render_template("despensa.html",datos=ingredientes)
	else:	
		AnadirIng(request.form["ingrediente"])
		return redirect("/despensa")

@app.route('/eliminar/<int:cod>')
def Eliminar(cod):
	with open ("usuarios/%s.json"%session["usuario"], "r") as datos:
		usuario=json.load(datos)
		usuario["ingredientes"].pop(cod)			
	with open ("usuarios/%s.json"%session["usuario"], "w") as datos:
		json.dump(usuario,datos)
	return redirect("/despensa")	

@app.route('/acercade')
def Acerca():
	return render_template("info.html")

if __name__ == '__main__':
	port=os.environ["PORT"]
	app.run('0.0.0.0',int(port), debug=True)