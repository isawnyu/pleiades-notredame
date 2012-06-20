## Script (Python) "userInByline"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=username
##title=
##
from Products.CMFCore.utils import getToolByName

mtool = getToolByName(context, 'portal_membership')
if username == 'T. Elliott': un = 'thomase'
elif username == 'S. Gillies': un = 'sgillies'
else: un = username
member = mtool.getMemberById(un)
if member:
    return {"id": member.getId(), "fullname": member.getProperty('fullname')}
else:
    return {"id": None, "fullname": un}

