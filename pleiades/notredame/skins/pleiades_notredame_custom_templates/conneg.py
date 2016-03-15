## Script (Python) "conneg"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

# Negotiate place view based on Accept request header.

# A mod_rewrite rule in Apache forwards requests to this script
# if it's a request for the default place view
# and the Accept header does not contain 'html' or equal '*/*'

from zExceptions import NotFound
from Products.PythonScripts.standard import html_quote

request = container.REQUEST
RESPONSE =  request.RESPONSE
RESPONSE.setHeader('Vary', 'Accept')

# the place
pid = request.get("pid")
if not pid or pid not in context.places:
    raise NotFound("Place %s cannot be found" % pid)

# parse accept header
user_preferences = []
for value in request.environ.get("HTTP_ACCEPT", "").split(","):
    parts = value.split(";")
    weight = 1.0
    if len(parts) == 2:
        try:
            weight = float(parts[1].split("=")[1])
        except:
            weight = 0.3
    user_preferences.append((weight, parts[0].strip()))
user_preferences.sort(reverse=True)

place = context.places[pid]
preferred = user_preferences[0][1]

if "text/turtle" in preferred or "application/turtle" in preferred:
    view = place.restrictedTraverse("@@turtle")
    RESPONSE.setStatus(200)
    RESPONSE.setHeader('Content-Location', place.absolute_url() + "/turtle")
    return view()
elif "application/rdf+xml" in preferred:
    view = place.restrictedTraverse("@@rdf")
    RESPONSE.setStatus(200)
    RESPONSE.setHeader('Content-Location', place.absolute_url() + "/rdf")
    return view()
elif "html" in preferred:
    view = place.restrictedTraverse("base_view")
    RESPONSE.setStatus(200)
    RESPONSE.setHeader('Content-Location', place.absolute_url())
    return view()
else:
    view = place.restrictedTraverse("conneg_406_message")
    RESPONSE.setStatus(200)
    return view(pid=pid)

