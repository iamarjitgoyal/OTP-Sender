from django.contrib import admin
from .models import Users


@admin.register(Users)
class AuthorAdmin(admin.ModelAdmin):
    pass