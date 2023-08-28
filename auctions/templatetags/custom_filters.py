from django import template

from auctions.models import category_names

# ===== Create a filter to access the choice dictionary in the for loop of index
register = template.Library()

@register.filter(name="get_category")
def get_category(dictionary, key):
    return dictionary.get(key)

# ======================================== Get list of full names for the navbar
@register.simple_tag
def get_category_names():
    return category_names
