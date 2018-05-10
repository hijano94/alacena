
<center>![](./templates/images/logo-ALC.png)</center>

# **ALaCena** 

## Introducción
**Alacena** pretende solventar esa gran duda que envuelve a todos los hogares. ***Que hacemos para comer?***  Alacena es una aplicación web que ofrece multiples recetas en función de los **ingredientes** que tengas en casa. El ususario solo tiene que acceder al sitio web de **Alacena** , introducir los ingredientes que tienen en casa y te aparecerán una variedad de recetas que podras preparar. 
Los usuarios también podrán registrarse en el sitio web y tener un registro de todos los ingredientes que tiene en casa, añadiedo o eliminando. De esta forma la aplicación podra hacer una busqueda más exaustiva y listar las recetas de la que dispongas todos los ingredientes. 

## Funcionalidad:
El usuario introducirá los filtros y los ingredientes que serán enviados a la aplicación mediante un metodo POST. Esta irá solicitando recetas a la API para cada uno de los ingredientes junto con los filtros, guardará los datos necesarios en un dict y los ordenará en función del número de ingredientes que coincidan con los que "tiene" el usuario y los mostrará de 10 en 10.

## APIs:
En principio solo voy a usar una API, la API de Edamam que devuelve recetas en función de los parametros que le envies como: Ingrediente, etiquetas de salud, calorias... Más adelante si voy bien de tiempo incorporaré una API de vision artificial para que el usuario pueda introducir también los ingredientes con fotos.
* [Edamam API](https://developer.edamam.com/es/api-recetas-edamam-documentacion) Devuelve los datos en *JSON* y tiene una autentificación de usuario y contraseñá en los parametros.

## Rutas:
* **/:** Pagina de inicio. Una pagina estática con un menú y varios enlaces que redirigiran al usuario a las distintas paginas de la web:
	* Buscador
	* Despensa
	* Acerca de (otra página estática que describe la funcionalidad de la web)
	* Repositorio de Github
* **/buscar** Buscador de recetas. Aqui el usuario rellenará el formulario que se enviará a la aplicación mediante un metodo POST y contendra: un filtro de busqueda para la API y Los ingredientes con los que se buscará el resultado más especifico. Si el usuario está registrado, aprte de los ingredientes que introduzca en el formulario se añadirán los que tenga guardados.
* **/resultados/<n pagina>** Listado de recetas encontradas y ordenadas de mayor numero de ingredientes introducidos a menor. Se muestran de 10 en 10 y al pasar a la siguiente pagina se solicitan las siguientes 10 a la aplicación.
* **/despensa/<usuario>** Listado de ingredientes guardados por un determinado usuario.	

## Hoja de estilo
La hoja de estilo *css* la he descargado de un proveedor gratuito de las mismas. [Templated](https://templated.co/) por lo que mi pagina será una pagina web válida.
