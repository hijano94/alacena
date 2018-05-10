import requests
import json
import os

URL="https://www.googleapis.com/customsearch/v1?parameters"

HEAD = {
'key':os.environ["google_key"],
'cx':'001650293485707683907:rnkqgsnoula', 
'q' : "pollo", 
#'searchType':'image',
'filter':'1' 
}

c=requests.get(URL ,params=HEAD)

resultados=c.json()
print(resultados)

## Más Parametros de Google
# imgSize (huge,icon,large,medium,samll,xlarge,xxlarge)
# imgType (clipart,face,lineart,news,photo)