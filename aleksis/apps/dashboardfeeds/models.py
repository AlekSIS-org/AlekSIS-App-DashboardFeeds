from typing import Optional

from django.utils.translation import ugettext_lazy as _

import feedparser

from django.db import models

from aleksis.core.models import DashboardWidget

from .util.html_helper import parse_rss_html
from .util.event_feed import get_current_events_with_cal


class RSSFeedWidget(DashboardWidget):
    template = "dashboardfeeds/rss.html"

    url = models.URLField(verbose_name=_("RSS Url"))
    base_url = models.URLField(verbose_name=_("Base URL"),
                               help_text=_("index url of the news website (as link for users)"))

    def get_context(self):
        result = feedparser.parse(self.url)["entries"][0]
        rich_text, img_href = parse_rss_html(result["summary"])
        if not img_href:
            img_href = result["enclosures"][0]["href"] if len(result["enclosures"]) > 0 else ""
        feed = {
            "title": self.title,
            "url": self.url,
            "base_url": self.base_url,
            "result": result,
            "img_href": img_href,
            "rich_text": rich_text,
        }
        return feed

    class Meta:
        verbose_name = _("RSS Widget")
        verbose_name_plural = _("RSS Widgets")


class ICalFeedWidget(DashboardWidget):
    template = "dashboardfeeds/ical.html"

    url = models.URLField(verbose_name=_("iCal URL"))
    base_url = models.URLField(verbose_name=_("Base URL"),
                               help_text=_("index url of the calendar (as link for users)"))
    events_count = models.IntegerField(verbose_name=_("number of displayed events"), default=5)

    def get_context(self):
        feed = {
            "base_url": self.base_url,
            "feed_events": get_current_events_with_cal(self.url, self.events_count),
        }
        return feed

    class Meta:
        verbose_name = _("Ical Widget")
        verbose_name_plural = _("Ical Widgets")
