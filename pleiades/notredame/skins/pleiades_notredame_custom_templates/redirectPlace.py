## Script (Python) "redirectPlace"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=pid
##title=
##
from Products.CMFCore.utils import getToolByName
rtool = getToolByName(context, 'portal_redirection')
return rtool.getRedirectsTo("places/" + str(pid))
