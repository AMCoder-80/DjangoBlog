from django import template

from ..models import Category, Article
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from star_ratings.models import Rating

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
def paginator_template(request, paginator, page_obj):
    context = {
        'request': request,
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


@register.inclusion_tag('registration/text_tag.html')
def text(status):
    context = {
        'status': status,
    }
    return context


@register.inclusion_tag('blog/top_articles.html')
def top_ones(state, header):
    if state == 'views':
        from_time = timezone.localtime(timezone.now()) - timedelta(days=30)
        query_set = Article.objects.annotate(
            count=Count('views', filter=Q(articleviews__created__gte=from_time))
        ).order_by('-count', '-published')[:3]
    elif state == 'controversial':
        query_set = Article.objects.annotate(
            count=Count('comments')
        ).order_by('-count', '-published')[:3]
    elif state == 'star':
        article_id = Rating.objects.all().order_by('-average', 'count')[:3]\
            .values_list('object_id', flat=True)
        query_set = list()
        for index in article_id:
            query_set.append(Article.objects.get(pk=index))

    context = {
    'article': query_set, # noqa
    'header': header,
    }

    return context
