from django.contrib import admin
from .models import (Gender, Category, Ingredient, Item)


# Register your models here.
admin.site.register(Gender)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Item)