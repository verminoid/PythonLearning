from django import template

register = template.Library()

@register.filter
def inc(value, arg):
    return int(value) + int(arg)

@register.inclusion_tag
def division(a,b, to_int=False):
    if to_int:
        return int(int(a)/int(b))
    else:
        return int(a)/int(b)
