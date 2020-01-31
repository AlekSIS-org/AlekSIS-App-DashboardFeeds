from typing import Optional

from django.utils.translation import ugettext_lazy as _

import feedparser

from django.db import models

from aleksis.core.models import DashboardWidget

from .util.html_helper import parse_rss_html


class RSSFeedWidget(DashboardWidget):
    template = "dashboardfeeds/rss.html"

    url = models.URLField(verbose_name=_("RSS Url"))
    base_url = models.URLField(verbose_name=_("Base URL"),
                               help_text=_("index url of the news website (as link for users)"))

    def get_context(self):
        result = feedparser.parse(self.url)["entries"][0]
        rich_text, img_href = parse_rss_html(result["summary"])
        img_href = img_href if img_href else result["enclosures"][0]["href"] if len(result["enclosures"]) > 0 else ""
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
