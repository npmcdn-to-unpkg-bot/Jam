# TEMPLATE FILTER REGISTERATIONS

from django import template

register = template.Library()

@register.filter
def underscore(album):
    return album.replace(' ', '_')