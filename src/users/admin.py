from django.contrib import admin

from src.users.models import CustomUser

admin.site.register(CustomUser)
