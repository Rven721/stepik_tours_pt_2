from django import template

register = template.Library()


@register.filter()
def star_display(stars):
    return '★' * int(stars)
