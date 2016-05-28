import urllib

from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.i18n import translate
from zope.publisher.browser import BrowserView

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.content.browser.tableview import Table, TableBrowserView
from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets.review import Renderer
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize


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


class FullReviewListView(BrowserView):

    def revlist(self):
        # apparently this is only used in a display condition
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(review_state='pending', sort_order='created')
        return brains

    def url(self):
        return self.context.absolute_url() + '/full_review_list'

    def review_table(self):
        table = ReviewListTable(self.context, self.request)
        return table.render()


class ReviewListTable(object):
    """
    The review list table renders the table and its actions.
    """

    def __init__(self, context, request, **kwargs):
        self.context = context
        self.request = request

        url = self.context.absolute_url()
        view_url = url + '/full_review_list'
        self.table = Table(request, url, view_url, self.items,
                           buttons=self.buttons)

    def render(self):
        return self.table.render()

    @property
    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        plone_utils = getToolByName(self.context, 'plone_utils')
        portal_url = getToolByName(self.context, 'portal_url')
        plone_view = getMultiAdapter((self.context, self.request),
                                     name=u'plone')
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        portal_properties = getToolByName(self.context, 'portal_properties')
        portal_types = getToolByName(self.context, 'portal_types')
        site_properties = portal_properties.site_properties

        use_view_action = site_properties.getProperty(
            'typesUseViewActionInListings', ())
        browser_default = self.context.browserDefault()

        results = list()
        brains = catalog(review_state='pending', sort_order='created')
        for i, obj in enumerate(brains):
            if i % 2 == 0:
                table_row_class = "even"
            else:
                table_row_class = "odd"

            url = obj.getURL()
            path = obj.getPath()
            icon = obj.getIcon
            icon_tag = '<img width="16" height="16" src="{}/{}" />'
            icon_tag = icon_tag.format(portal_url(), icon)

            type_class = 'contenttype-' + plone_utils.normalizeString(
                obj.portal_type)

            review_state = 'Pending review'

            state_class = 'state-' + plone_utils.normalizeString(review_state)
            #relative_url = portal_url.getRelativeContentURL(obj)

            type_title_msgid = portal_types[obj.portal_type].Title()
            url_href_title = u'%s: %s' % (translate(type_title_msgid,
                                                    context=self.request),
                                          safe_unicode(obj.Description))

            modified = plone_view.toLocalizedTime(
                obj.modified, long_format=1)
            is_structural_folder = False

            if obj.portal_type in use_view_action:
                view_url = url + '/view'
            elif is_structural_folder:
                view_url = url + "/folder_contents"
            else:
                view_url = url

            is_browser_default = len(browser_default[1]) == 1 and (
                obj.getId == browser_default[1][0])

            results.append(dict(
                url=url,
                url_href_title=url_href_title,
                id=obj.getId,
                quoted_id=urllib.quote_plus(obj.getId),
                path=path,
                title_or_id=obj.Title,
                description=obj.Description,
                obj_type=obj.Type,
                size=obj.getObjSize,
                modified=modified,
                icon=icon_tag,
                type_class=type_class,
                wf_state=review_state,
                state_title=portal_workflow.getTitleForStateOnType(
                    review_state, obj.portal_type),
                state_class=state_class,
                is_browser_default=is_browser_default,
                folderish=is_structural_folder,
                relative_url='',
                view_url=view_url,
                table_row_class=table_row_class,
                is_expired=False
            ))
        return results

    @property
    def show_sort_column(self):
        return False

    def buttons(self):
        buttons = []
        portal_actions = getToolByName(self.context, 'portal_actions')
        button_actions = portal_actions.listActionInfos(
            object=aq_inner(self.context), categories=('folder_buttons',))

        # Do not show buttons if there is no data, unless there is data to be
        # pasted
        if False:  # not len(self.batch):
            if self.context.cb_dataValid():
                for button in button_actions:
                    if button['id'] == 'paste':
                        return [self.setbuttonclass(button)]
            else:
                return []

        for button in button_actions:
            # Make proper classes for our buttons
            if button['id'] != 'paste' or self.context.cb_dataValid():
                buttons.append(self.setbuttonclass(button))
        return buttons

    def setbuttonclass(self, button):
        if button['id'] == 'paste':
            button['cssclass'] = 'standalone'
        else:
            button['cssclass'] = 'context'
        return button
