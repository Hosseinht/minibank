from django.contrib import admin

from .models import Category, Currency, Transaction


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Currency)
admin.site.register(Transaction)
