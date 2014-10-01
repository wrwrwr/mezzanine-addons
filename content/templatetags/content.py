from mezzanine import template
from mezzanine.core.templatetags.mezzanine_tags import thumbnail

from ..models import Banner


register = template.Library()


@register.simple_tag
def image(content, width, height):
    if not content.image_scaling:
        return content.image
    if content.image_width or content.image_height:
        width = content.image_width
        height = content.image_height
    return thumbnail(content.image, width, height, int(content.image_quality))


@register.inclusion_tag('banner.html')
def banner(key, width, height):
    context = {'key': key}
    try:
        banner = Banner.objects.get(key=key)
    except Banner.DoesNotExist:
        pass
    else:
        context['image'] = image(banner, width, height)
        context['link'] = banner.link
    return context
