## Script (Python) "limitedQueryCatalog"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFPlone.PloneBatch import Batch

limited = context.getLimitNumber()
if limited:
    n = int(context.getItemCount()) or 20
    return Batch(context.queryCatalog(), n, 0)
else:
    return context.queryCatalog(batch=True)

