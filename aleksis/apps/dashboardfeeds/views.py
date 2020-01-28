from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import DashboardWidget


@login_required
def empty(request: HttpRequest) -> HttpResponse:
    context = {}

    return render(request, "dashboardfeeds/empty.html", context)


def get_widgets(request):
    widgets = DashboardWidget.objects.all()

    widgets_to_return = []

    for widget in widgets:
        feed = widget.widget.get_feed()

        # widgets_to_return.append(render_to_string(widget.widget.template, feed, request))
        widgets_to_return.append((widget.widget.template, feed))

    return widgets_to_return
