from mezzanine.pages.page_processors import processor_for

try:
    # The module is meant to be usable without cartridge.
    from cartridge.shop.models import Category
except ImportError:
    from mezzanine.pages.models import Page as Category

from .models import Section


@processor_for(Section)
def section_processor(request, page):
    subpages = page.section.children.published()
    child_categories = Category.objects.filter(id__in=subpages)
    return {'child_categories': child_categories}
