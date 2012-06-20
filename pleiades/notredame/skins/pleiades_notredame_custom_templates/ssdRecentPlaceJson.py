## Script (Python) "ssdRecentPlaceJson"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from random import choice, sample

request = container.REQUEST
RESPONSE =  request.RESPONSE
RESPONSE.setHeader("Cache-Control", "max-age=6")
RESPONSE.setHeader("Access-Control-Allow-Origin", "*")

results = []
recent = context.recentPids()
key = choice(recent)
results.append(context.places[key].restrictedTraverse("@@json")(published_only=True))
for key in sample(context.places.keys(), 10):
    try:
        pid = int(key)
        results.append(context.places[key].restrictedTraverse("@@json")(published_only=True))
        break
    except ValueError:
        continue
if len(results) < 2:
    results.append(context.places['1043'].restrictedTraverse("@@json")(published_only=True))
    
return '{"limit": %s, "results": [%s]}' % (30, ",".join(results))

