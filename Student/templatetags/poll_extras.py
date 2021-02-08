from django import template

register = template.Library()


@register.simple_tag
def my_custom_boolean_filter(val):
    return val
