# TEMPLATE FILTER REGISTERATIONS

from django import template

register = template.Library()

@register.filter
def underscore(album):
    album = album.replace(' ', '_')
    return album.lower()