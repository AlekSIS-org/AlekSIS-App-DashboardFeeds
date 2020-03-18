# Generated by Django 3.0.4 on 2020-03-18 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_auto_20190901_1644'),
        ('dashboardfeeds', '0002_icalfeedwidget'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssfeedwidget',
            name='rss_source',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='feeds.Source', verbose_name='Rss Source'),
        ),
    ]
