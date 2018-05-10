from flask import Flask
from flask import render_template,request,redirect,session
import json



###########################################
                 MAIN
###########################################
@app.route('/')
def inicio():
	return render_template("index.html")

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
	if request.method=="GET":
		return render_template("addeventos.html",datos=None,error=None,boton="Crear Evento",url="/eventos/add")
	else:
		titulo = request.form['titulo']   
		return redirect("/resultados")

if __name__ == '__main__':
	app.debug = True
	app.run()