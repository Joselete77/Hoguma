"""
In this file we create the classes that we want to be translated
"""

from modeltranslation.translator import translator, TranslationOptions
from .models import *


class promotionTranslation(TranslationOptions):
    fields = ('name', 'description')

class typeRoomHotelTranslation(TranslationOptions):
    fields = ('name', 'description')

translator.register(promotion, promotionTranslation)
translator.register(typeRoomHotel, typeRoomHotelTranslation)
