from django import template
import re

# Registering a template object
register = template.Library()


# Decorating the method as a filter
@register.filter(name='no_image')
def image_remover(value):
    pattern = r'(<img[^>]*>)\s*|(<table.*?</table>)\s*'
    pattern_par = r'(<p.*?>)(.*?)(</p>)'
    result = re.sub(pattern, '', value)
    result = re.sub(pattern_par, r'\2', result)
    return result.strip()