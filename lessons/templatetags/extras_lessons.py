from django import template
from lessons.models import Chapter


register = template.Library()


@register.filter(name='get_by_order')
def order(chapter: Chapter) -> int:
   return chapter.content_set.order_by('content_order')
