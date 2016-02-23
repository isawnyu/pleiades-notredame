## Script (Python) "sortCredits"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=credits, sort_on
##title=
##
if not sort_on:
    return credits
if sort_on in ('count'):
    credits.sort(key=lambda x: int(x[sort_on]), reverse=True)
else:
    credits.sort(key=lambda x: x[sort_on])
return credits
