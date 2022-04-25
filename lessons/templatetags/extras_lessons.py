"""
modul rozšiřující funkcionality šablonovacího systému JINJA


@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""

from django import template
from lessons.models import Chapter


register = template.Library()


@register.filter(name='get_by_order')
def order(chapter: Chapter) -> int:
   """ filter vrací data z databáze. Vrací pořadí Kapitly'

       @param chapter: Kapitola

       @return pořadí kapitoly
       """
   return chapter.content_set.order_by('content_order')
