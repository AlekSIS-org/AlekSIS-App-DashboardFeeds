# Generated by Django 3.0.4 on 2020-03-28 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboardfeeds", "0003_rssfeedwidget_rss_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="rssfeedwidget",
            name="text_only",
            field=models.BooleanField(default=False, verbose_name="Text Only RSS Feed"),
        ),
    ]
