__author__ = 'ximepa'
from django import template

register = template.Library()

@register.filter
def in_queues(things, queue):
    return things.filter(queue=queue)