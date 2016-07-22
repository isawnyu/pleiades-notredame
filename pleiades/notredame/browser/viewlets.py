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
    """

    index = ViewPageTemplateFile('templates/rich_meta.pt')

    def update(self):
        super(RichMetaViewlet, self).update()

    def title(self):
        return self.context.Title()

    def formatted_title_and_content_type(self):
        title = self.context.Title()
        ct = self.context.Type()
        return title + ': a Pleiades '+ ct + ' resource'

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

    def creators(self):
        """ return list of creator's fullnames
        """
        creators = []
        mt = getToolByName(self.context, 'portal_membership')
        creators_tuple = self.context.listCreators()
        for username in creators_tuple:
            member = mt.getMemberById(username)
            if member is not None:
                creators.append(member.getProperty("fullname"))
            else:
                creators.append(username)
        return creators

    def contributors(self):
        """ return list of contributor's fullnames            
        """
        contributors = []
        mt = getToolByName(self.context, 'portal_membership')
        contributors_tuple = self.context.listContributors()
        for username in contributors_tuple:
            member = mt.getMemberById(username)
            if member is not None:
                contributors.append(member.getProperty("fullname"))
            else:
                contributors.append(username)
        return contributors
