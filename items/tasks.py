from __future__ import absolute_import, unicode_literals

from datetime import timedelta, datetime

from celery import shared_task

from .models import Lgtm, Item, PopularItem


@shared_task
def assemble_popular_item():
    """
    最近LGTMを受け取ったItemをまとめる
    """
    lgtm_time = datetime.now() - timedelta(hours=12)

    lgtms = Lgtm.objects.filter(created_at__gte=lgtm_time)
    lgtms_ids = lgtms.values_list('item_id', flat=True)

    items = Item.objects.filter(id__in=lgtms_ids)

    PopularItem.objects.all().delete()

    PopularItem.objects.bulk_create(
        PopularItem(item=item, lgtm_count=lgtms.filter(item=item).count())
        for item in items
    )

    pass
