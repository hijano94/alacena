# ALaCena

## Introducción
**Alacena** pretende solventar esa gran duda que envuelve a todos los hogares. ***Que hacemos para comer?***  Alacena es una aplicación web que ofrece multiples recetas en función de los **ingredientes** que tengas en casa. El ususario solo tiene que acceder al sitio web de **Alacena** , introducir los ingredientes que tienen en casa y te aparecerán una variedad de recetas que podras preparar. 
Los usuarios también podrán registrarse en el sitio web y tener un registro de todos los ingredientes que tiene en casa, añadiedo o eliminando. De esta forma la aplicación podra hacer una busqueda más exaustiva y listar las recetas de la que dispongas todos los ingredientes. 

## Funcionalidad:



## APIs:
* [Edamam API](https://developer.edamam.com/es/api-recetas-edamam-documentacion) API capaz de devolver recetas en función de un ingrediente. *JSON*
* **Visión artificial?** para introducir ingredientes mediante fotos
* **Google Images?** ponerle foto a los ingredientes

## Rutas:
* **/:** Pagina de inicio.
* **/buscar** Buscador de recetas. Formulario con los requisitos de la petición.
* **/resultados/<n pagina>** Listado de recetas encontradas. Se muestran de 10 en 10 y al pasar a la siguiente pagina se solicitan las siguientes 10 a la API.
* **/despensa/<usuario>** Listado de ingredientes guardados por un determinado usuario.	

## Hoja de estilo
La hoja de estilo *css* la he descargado de un proveedor gratuito de las mismas. [Templated](https://templated.co/) por lo que mi pagina será una pagina web válida.
