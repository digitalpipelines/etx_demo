from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeIngredientImage
from django.contrib.auth import get_user_model

User = get_user_model()

## It possible to add other things to the user manager ##
# admin.site.unregister(User)

# class RecipeInline(admin.StackedInline):
#     model = Recipe
#     extra = 1

# class UserAdmin(admin.ModelAdmin):
#     inlines = [RecipeInline]
#     list_display = ['username']

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 1

class RecipeIngredientAdmin(admin.ModelAdmin):    
    list_display = ['name']
    readonly_fields = ['quanity_as_float','as_mks', 'as_imperial']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeIngredientImage)