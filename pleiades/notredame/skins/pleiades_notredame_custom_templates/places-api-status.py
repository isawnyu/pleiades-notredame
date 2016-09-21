## Script (Python) "places-api-status"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = container.REQUEST
RESPONSE =  request.RESPONSE
RESPONSE.setHeader("Cache-Control", "max-age=3600")
RESPONSE.setHeader("Access-Control-Allow-Origin", "*")
RESPONSE.setHeader("Content-Type", "application/json")

types_count = context.countType()
for k, v in types_count.items():
    v = str(v).replace(",", "")
    types_count[k] = int(v)

return ''.join([
    '{',
    '"num_places": %(num_places)d, "num_locations": %(num_locations)d, "num_names": %(num_names)d, ' % types_count,
    '"slideshow_data": {"recent": "https://pleiades.stoa.org/ssdRecentPlaceJson", "any": "https://pleiades.stoa.org/ssdAnyPlaceJson"}',
    '}' ])
