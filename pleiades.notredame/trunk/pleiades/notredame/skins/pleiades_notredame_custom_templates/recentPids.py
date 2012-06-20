## Script (Python) "recentPids"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
catalog = container.portal_catalog
return [b.getId for b in catalog.searchResults(
    portal_type='Place', review_state='published', sort_on='modified', sort_order='descending', sort_limit=20)[:20]]

