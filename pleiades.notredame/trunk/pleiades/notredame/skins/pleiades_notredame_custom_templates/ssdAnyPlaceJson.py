## Script (Python) "ssdAnyPlaceJson"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from random import sample

request = container.REQUEST
RESPONSE =  request.RESPONSE
RESPONSE.setHeader("Cache-Control", "max-age=6")
RESPONSE.setHeader("Access-Control-Allow-Origin", "*")

results = []
while 1:
    a, b = sample(context.places.keys(), 2)
    try:
        pid = int(a)
        results.append(context.places[a].restrictedTraverse("@@json")(published_only=True))
        pid = int(b)
        results.append(context.places[b].restrictedTraverse("@@json")(published_only=True))
        break
    except ValueError:
        continue
    
return '{"limit": %s, "results": [%s]}' % (70, ",".join(results))

