## Script (Python) "getPlaceFacets"
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

indexes = {
    "Location Precision": 'location_precision',
    "Place Type": 'getFeatureType',
    "Time Periods": 'getTimePeriods'
    }
vocabs = {
    "Location Precision": ["unlocated", "rough", "precise"],
    "Place Type": 'place-types',
    "Time Periods": 'time-periods'
    }

portalurl = context.portal_url()
portal = context.portal_url.getPortalObject()
vtool = context.portal_vocabularies
wftool = context.portal_workflow
catalog = context.portal_catalog

basequery = {'portal_type': 'Place', 'review_state': 'published'}

data = {}
sortedlabels = indexes.keys()
sortedlabels.sort()
data['sortedLabels'] = sortedlabels[:]

for label, index in indexes.items():

    if label == "Location Precision":
        values = vocabs[label]
    else:
        terms = portal.restrictedTraverse('vocabularies/' + vocabs[label]).terms
        terms = {term['id']: term for term in terms}
        values = catalog.uniqueValuesFor(index)

    data[label] = []
    
    for v in values:
        query = basequery.copy()
        query[index] = v
        if label == "Location Precision":
            tval = v
        else:
            term = vocab.get(v, None)
            if term is not None:
                tval = term['title']
            else:
                tval = "Erroneous (%s)" % v

        results = catalog(query)
        
        item = dict(
            label=label,
            value=tval,
            count=len(results),
            details="%s/search?portal_type=Place&%s=%s" % (
                portalurl, index, v),
        )
        if len(results) <= 100:
            item['details'] = "%s/search?portal_type=Place&sort_on=sortable_title&%s=%s" % (portalurl, index, v)
        else:
            # subqueries using titleStarts index
            item['groups'] = []
            for group in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                chars = [char for char in group]
                query['titleStarts'] = chars
                results = catalog(query, sort_on='sortable_title')
                
                tqs = '&'.join(["titleStarts:list=%s" % char for char in chars])

                item['groups'].append(
                    dict(
                        label=label,
                        value=group,
                        count=len(results),
                        details="%s/search?portal_type=Place&sort_on=sortable_title&%s=%s&%s" % (
                            portalurl, index, v, tqs)
                    ))

        data[label].append(item)
        cmpfunc=lambda x, y: cmp(x['value'], y['value'])
        data[label].sort(cmp=cmpfunc)

return data

