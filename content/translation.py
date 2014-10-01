import mezzanine.core.translation
import mezzanine.pages.translation

from modeltranslation.translator import TranslationOptions, translator

from .models import Banner, Partner, ImagePage, Section


class BannerTranslationOptions(TranslationOptions):
    fields = ('link',)


class PartnerTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'website',)


translator.register(Banner, BannerTranslationOptions)
translator.register(Partner, PartnerTranslationOptions)
translator.register((ImagePage, Section))

