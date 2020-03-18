from django.contrib import admin

from .models import DashboardWidget, RSSFeedWidget, ICalFeedWidget

admin.site.register(DashboardWidget)
admin.site.register(RSSFeedWidget)
admin.site.register(ICalFeedWidget)
