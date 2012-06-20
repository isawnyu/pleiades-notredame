## Script (Python) "flickrTagged"
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
url = "http://www.flickr.com/photos/tags/pleiades:*=%s/" % context.getId()
RESPONSE.redirect(url)

