## Script (Python) "randomPid"
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
RESPONSE.setHeader("x-header-set-id", "no-cache")

keys = context.places.keys()
# keys = ['foo', 'bar', '1', 'bar']
while 1:
    pick = choice(keys)    
    try:
        return int(pick)
    except ValueError:
        pass

