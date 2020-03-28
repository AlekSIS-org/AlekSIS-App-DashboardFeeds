from feeds.utils import update_feeds

from aleksis.core.util.core_helpers import celery_optional


@celery_optional
def get_feeds():
    update_feeds(10)
