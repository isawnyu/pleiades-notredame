## Script (Python) "randomPlaceJson"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from random import choice

request = container.REQUEST
RESPONSE =  request.RESPONSE
# RESPONSE.setHeader("X-Header-Set-Id", "no-cache")
RESPONSE.setHeader("Cache-Control", "max-age=6")
RESPONSE.setHeader("Access-Control-Allow-Origin", "*")

keys = context.places.keys()
while 1:
    pick = choice(keys) 
    try:
        pid = int(pick)
        return container["places"][pick].restrictedTraverse("@@json")() 
    except ValueError:
        pass

