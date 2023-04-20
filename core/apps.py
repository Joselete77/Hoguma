"""
This file, created by Django, helps to include any configuration of the application. 
It can be used to configure some of the attributes of the application.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
