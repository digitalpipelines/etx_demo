from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Recipe, RecipeIngredient
from django.core.exceptions import ValidationError

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('test_user', password='123')

    def test_user_pw(self):
        checked = self.user_a.check_password('123')
        self.assertTrue(checked)    


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('test_user', password='123')
        self.recipe_a = Recipe.objects.create(
            name ='Test Receipe',
            user = self.user_a
        )
        self.recipe_b = Recipe.objects.create(
            name ='Test Receipe B',
            user = self.user_a
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            name = 'ingredient a',
            quanity = '1',
            unit = 'pound',
            recipe = self.recipe_a
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            name = 'ingredient b',
            quanity = 'giberish',
            unit = 'giberish....shshsh',
            recipe = self.recipe_a
        )
            
        

    def test_user(self):    
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 2)  

    def test_receipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(), 2)       

    def test_unit_measure_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quanity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quanity_as_float)

    def test_unit_of_measure_validation(self):
        invalidUnits = ['blah', 'yada']
        with self.assertRaises(ValidationError):
            for unit in invalidUnits:
                ingredient = RecipeIngredient(
                    name='new',
                    quanity=10,
                    recipe = self.recipe_a,
                    unit=unit
                )
                ingredient.full_clean()

