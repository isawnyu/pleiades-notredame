## Script (Python) "fixedCreators"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
creators = list(context.Creators())
contributors = context.Contributors()
if "sgillies" in creators and ("sgillies" in contributors or "S. Gillies" in contributors):
    creators.remove("sgillies")
return creators

