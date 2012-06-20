## Script (Python) "reprPt"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
return context.restrictedTraverse("@@json/data_uri")

