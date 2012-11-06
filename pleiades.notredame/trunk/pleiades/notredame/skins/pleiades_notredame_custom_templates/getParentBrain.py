## Script (Python) "getParentBrain"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=rec
##title=
##
from Products.CMFCore.utils import getToolByName

catalog = getToolByName(context, 'portal_catalog')
results = catalog(
    path="/".join(rec.getPath().split("/")[:-1]), portal_type="Place" )
return results and results[0] or None

