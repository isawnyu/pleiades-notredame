## Script (Python) "getCredits"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
import DateTime
from Products.CMFCore.utils import getToolByName

fake_users = ['auser', 'juser']

catalog = getToolByName(context, 'portal_catalog')
mtool = getToolByName(context, 'portal_membership')

contributors = list(catalog.uniqueValuesFor('Contributors'))
for u in catalog.uniqueValuesFor('Creator'):
    if not u in contributors:
        contributors.append(u)
contributors.remove('sgillies')
contributors.remove('thomase')
contributors.remove('rtalbert')
contributors.remove('admin')

data = {}

for user in filter(lambda x: x is not None, map(mtool.getMemberById, contributors)):
    username = user.getUserName()
    if username in fake_users:
        continue
    a = len(catalog(Contributors=username, review_state="published"))
    b = len(catalog(Creator=username, review_state="published"))
    if a > 0 or b > 0:
        fullname = user.getUser().getProperty('fullname')
        roles = user.getRoles()
        for r in ['Member', 'Contributor', 'Authenticated']:
            if r in roles:
                roles.remove(r)
        roles.append('Member')
        roles = ", ".join(roles[~2:~0]) + "; "*bool(len(roles)-1) + roles[-1]
        try:
            creation_date = context.restrictedTraverse("/plone/Members/" + username).CreationDate()
            start = DateTime.DateTime(creation_date)
            start_date = "%s %s %s" % (start.day(), start.Month(), start.year())
        except:
            creation_date = ""
            start_date = ""
        data[fullname] = {
            'fullname': fullname,
            'username': username,
            'roles': roles,
            'start_date': start_date,
            'start': creation_date,
            'count': a + b,
            'contributed': a,
            'authored': b,
            'portrait': mtool.getPersonalPortrait(username).absolute_url() }

keys = data.keys()
keys.sort()
return [data[k] for k in keys]
