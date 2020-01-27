from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import feedparser

from constance import config

from aleksis.core.util import network


class DashboardWidget(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Widget Title"))
    active = models.BooleanField(blank=True, verbose_name=_("Activate Widget"))
    base_url = models.URLField(verbose_name=_("Base URL"),
                               help_text=_("index url of the news website (as link for users)"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Dashboard Widget")
        verbose_name_plural = _("Dashboard Widgets")


# class WordpressFeedWidget(models.Model):
#     widget = models.OneToOneField(DashboardWidget, related_name="widget", verbose_name=_("widget"),
#                                   on_delete=models.CASCADE)
#     url = models.URLField(verbose_name=_("Wordpress Url"))
# filter_vs_composer = models.BooleanField(verbose_name=_("Filter out Visual Composer Tags?"), blank=True, default=True)
#
#     # author_whitelist: list = None,
#     # author_blacklist: list = None,
#     # category_whitelist: list = None,
#     # category_blacklist: list = None,
#
#     # https://wordpress.org/support/article/wordpress-feeds/#finding-your-feed-url
#
#     def get_feed(self):
#         feed = {
#             "title": self.widget.title,
#             "active": self.widget.active,
#             "url": self.url,
#             "results": network.get_newest_articles(domain=self.url, ),
#         }
#
#     class Meta:
#         verbose_name = _("Wordpress Widget")
#         verbose_name_plural = _("Wordpress Widgets")


class RSSFeedWidget(models.Model):
    template = "dashboardfeeds/rss.html"

    widget = models.OneToOneField(DashboardWidget, related_name="widget", verbose_name=_("widget"),
                                  on_delete=models.CASCADE)
    url = models.URLField(verbose_name=_("RSS Url"))

    def get_feed(self):
        feed = {
            "title": self.widget.title,
            "active": self.widget.active,
            "url": self.url,
            "base_url": self.widget.base_url,
            "result": feedparser.parse(self.url)["entries"][0],
        }
        return feed

    class Meta:
        verbose_name = _("RSS Widget")
        verbose_name_plural = _("RSS Widgets")
