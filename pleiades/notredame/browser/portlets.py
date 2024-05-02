from datetime import datetime
from DateTime import DateTime
from DateTime.interfaces import DateTimeError
from plone.app.portlets.portlets.rss import FEED_DATA
from plone.app.portlets.portlets.rss import Renderer as RSSRenderer
from plone.app.portlets.portlets.rss import RSSFeed
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile


class PleiadesRSSFeed(RSSFeed):

    def _buildItemDict(self, item):
        # Don't error when title is missing, add formatted pubdate
        link = item.links[0]['href']
        title = item.get('title')
        if not title:
            pubdate = datetime(*item.published_parsed[:7])
            pubdate = pubdate.strftime("%d %B %Y")
        itemdict = {
            'title': title,
            'pubdate': pubdate,
            'url': link,
            'summary': item.get('description', ''),
        }
        if hasattr(item, "updated"):
            try:
                itemdict['updated'] = DateTime(item.updated)
            except DateTimeError:
                # It's okay to drop it because in the
                # template, this is checked with
                # ``exists:``
                pass

        return itemdict


class PleiadesRSSRenderer(RSSRenderer):

    render_full = ZopeTwoPageTemplateFile('templates/rss.pt')

    def _getFeed(self):
        # Use our custom feed generator class
        feed = FEED_DATA.get(self.data.url, None)
        if feed is None:
            # create it
            feed = FEED_DATA[self.data.url] = PleiadesRSSFeed(self.data.url, self.data.timeout)
        return feed