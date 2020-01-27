from django.contrib import admin

from .models import DashboardWidget, RSSFeedWidget

admin.site.register(DashboardWidget)
admin.site.register(RSSFeedWidget)
