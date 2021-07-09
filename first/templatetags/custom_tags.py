from django import template
from ..models import Category

register = template.Library()

# Here we define the type of tag and its functionality
@register.simple_tag
def add_title(data='Rocket Article'):
    return data

# Here we defined a inclusion tag which works like this:
# When this tag called, the template engine renders another template by desire data which we send to it
# By this function
@register.inclusion_tag('first/navbar.html')
def nav_items():
    category = Category.objects.all()
    return {'category': category}