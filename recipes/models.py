import pathlib
import uuid
from django.db import models
from django.conf import settings
from django.db import models
from .validators import validate_unit_of_measure
from .utils import number_str_to_float
import pint
from django.urls import reverse
from django.db.models import Q

USER = settings.AUTH_USER_MODEL

class RecipeQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == '':
            return self.none()
        lookups = (
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(description__icontains=query)
        )
        return self.filter(lookups)

class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self.db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions =  models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = RecipeManager()

    @property
    def title(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('recipes:delete', kwargs={'id': self.id})          

    def get_hx_url(self):
        return reverse('recipes:hx-detail', kwargs={'id': self.id})       

    def get_edit_url(self):
        return reverse('recipes:update', kwargs={'id': self.id})     
    
    def get_ingredients_children(self):
        return self.recipeingredient_set.all()    

def recipe_ingredient_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) # uuid1 -> uuid + timestamps
    return f"recipes/ingredient/{new_fname}{fpath.suffix}"

         
class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=recipe_ingredient_image_upload_handler) #path/to/the/file.png
    extracted = models.JSONField(blank=True, null=True)
    #file_test = models.FileField(upload_to='files/')

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quanity = models.CharField(max_length=50)
    quanity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure])
    directions =  models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def get_delete_url(self):
        kwargs = {
            'parent_id': self.recipe.id,
            'id': self.id
        }
        return reverse('recipes:ingredient-delete', kwargs=kwargs)         

    def get_hx_edit_url(self):
        kwargs = {
            'parent_id': self.recipe.id,
            'id': self.id
        }
        return reverse('recipes:hx-ingredient-update', kwargs=kwargs) 

    def convert_to_system(self, system='mks'):
        ureg = pint.UnitRegistry(system=system)
        measurment = self.quanity_as_float * ureg[self.unit]
        return measurment

    def as_mks(self):
        if self.quanity_as_float is None:
            return ''
        measurment = self.convert_to_system(system='mks')
        return measurment.to_base_units()

    def as_imperial(self):
        if self.quanity_as_float is None:
            return ''
        measurment = self.convert_to_system(system='imperial')
        return measurment.to_base_units()

    def save(self, *args, **kwargs):
        qty = self.quanity
        qty_float, qty_float_success = number_str_to_float(qty)
        if qty_float_success: 
            self.quanity_as_float = qty_float
        else:
            self.quanity_as_float = None    
        super().save(*args, **kwargs)  
