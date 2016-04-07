from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from zope.component import queryUtility

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets.review import Renderer


class ReviewPortlet(Renderer):

    render = ViewPageTemplateFile('templates/review.pt')

    title = _('box_review_list', default=u"Review List")

    @memoize
    def _data(self):
        if self.anonymous:
            return []
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')
        catalog = getToolByName(context, 'portal_catalog')

        plone_view = getMultiAdapter((context, self.request), name='plone')
        getMember = getToolByName(context, 'portal_membership').getMemberById
        getIcon = plone_view.getIcon
        toLocalizedTime = plone_view.toLocalizedTime

        idnormalizer = queryUtility(IIDNormalizer)
        norm = idnormalizer.normalize
        brains = catalog(review_state='pending', sort_order='created')
        items = []
        for brain in brains[:20]:
            obj = brain.getObject()
            review_state = workflow.getInfoFor(obj, 'review_state')
            creator_id = obj.Creator()
            creator = getMember(creator_id)
            if creator:
                creator_name = creator.getProperty('fullname', '') or creator_id
            else:
                creator_name = creator_id

            items.append(dict(
                path = obj.absolute_url(),
                title = obj.pretty_title_or_id(),
                description = obj.Description(),
                icon = getIcon(obj).html_tag(),
                creator = creator_name,
                review_state = review_state,
                review_state_class = 'state-%s ' % norm(review_state),
                mod_date = toLocalizedTime(obj.ModificationDate()),
            ))
        return items
