from django import template
from django.template.defaultfilters import register

@register.filter(name='get_item')
def get_item(dictionary, index):
    if index in dictionary:
        return dictionary[index]
    return ''

@register.filter(name='a_sub_b')
def a_sub_b(a, b):
    return a-b

@register.filter(name='here')
def here(a):
    if a in [3, 6, 9, 12]:
        return True
    return False