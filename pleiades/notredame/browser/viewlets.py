from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from plone.memoize.instance import memoize

class PathBarViewlet(common.PathBarViewlet):
    """Customized breadcrumbs class
    """
    
    render = ViewPageTemplateFile('templates/pathbar.pt')


class RichMetaViewlet(common.ViewletBase):
    """ Viewlet that embedds rich bibliography data on each page
        note: template also makes use of methods from @@credit_utils view
    """

    index = ViewPageTemplateFile('templates/rich_meta.pt')

    def update(self):
        super(RichMetaViewlet, self).update()

    def title(self):
        return unicode(self.context.Title(), 'utf-8')

    def last_modified_date(self):
        # formatted ISO 8601 """
        return self.context.modified().ISO()

    def description(self):
        return self.context.Description()

    def rights(self):
        return self.context.Rights()

    @memoize
    def canonical_uri(self):
        return self.context.absolute_url()
