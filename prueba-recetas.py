import requests
import json
import os

# export recipe_id="865df3ed"
# export recipe_key="4f51c661f21a9d672cf8a8b2caeaa4ee"

#### VARIABLES GLOBALES ####
URL="https://test-es.edamam.com/search"
HEAD = {'app_id':os.environ["recipe_id"],'app-key': os.environ["recipe_key"], 'q' : "pollo"}

#### FUNCIONES ####
payload= {'q' : "chicken"}	
c=requests.get(URL ,headers=HEAD)

print("c: ",c.text)
print(c.headers['content-type'])



if c.status_code == 200:
	recetas=c.json()
	print(recetas)

else:
	print("API no disponible...")	
