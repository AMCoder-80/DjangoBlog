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
@register.inclusion_tag('blog/navbar.html')
def nav_items():
    category = Category.objects.filter(status=True, parent=None)
    return {'category': category}


@register.inclusion_tag('blog/paginator.html')
def paginator_template(paginator, page_obj):
    context = {
        'articles': page_obj,
        'paginator': paginator,
    }
    return context


@register.inclusion_tag('AdminLTE/links.html')
def link(request, url_name, link_name, style):
    context = {
        'request': request,
        'url_name': url_name,
        'link': f'accounts:{url_name}',
        'link_name': link_name,
        'style': style,
    }
    return context


@register.inclusion_tag('AdminLTE/status.html')
def status(user, status, article):
    context = {
        'user': user,
        'status': status,
        'article': article,
    }
    return context