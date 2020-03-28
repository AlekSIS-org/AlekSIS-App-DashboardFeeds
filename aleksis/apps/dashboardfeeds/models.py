import datetime
from typing import Optional

from django.db import models
from django.utils.translation import gettext_lazy as _

from feeds.models import Source

from aleksis.core.models import DashboardWidget

from .util.event_feed import get_current_events_with_cal


class RSSFeedWidget(DashboardWidget):
    template = "dashboardfeeds/rss.html"

    url = models.URLField(verbose_name=_("RSS Url"))
    base_url = models.URLField(verbose_name=_("Base URL"),
                               help_text=_("index url of the news website (as link for users)"))
    rss_source = models.ForeignKey(Source, verbose_name=_("Rss Source"), on_delete=models.CASCADE, editable=False,
                                   null=True)

    def save(self, *args, **kwargs):
        if not self.rss_source:
            source = Source()
            source.name = self.title
            source.feed_url = self.url
            source.site_url = self.base_url

            source.last_success = datetime.datetime.utcnow()
            source.last_change = datetime.datetime.utcnow()

            source.save()

            self.rss_source = source

        self.rss_source.live = self.active
        self.rss_source.save()

        super().save()

    def get_context(self):
        posts = self.rss_source.posts.all().order_by("-created")
        post = posts[0] if len(posts) > 0 else None
        feed = {
            "title": self.title,
            "url": self.rss_source.feed_url,
            "base_url": self.rss_source.site_url,
            "result": post,
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
