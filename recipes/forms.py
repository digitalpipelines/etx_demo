from django import forms
from .models import Recipe, RecipeIngredient, RecipeIngredientImage


class RecipeIngredientImageForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredientImage
        fields = ['image']

class RecipeForm(forms.ModelForm):
   # error_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 
    "placeholder":"Recipe Name"}), help_text='This is help for this field <a href="/contact">Contact Us - example</a>') #Like in bootstrap 
    # description = forms.CharField(widget=forms.Textarea (attrs={"rows":3}))
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'class': 'form-control-2'})  
        for field in self.fields:
            new_data = {    
                "placeholder": f'Recipe {str(field)}',
                "class":'form-control',
                # "hx-post":'.',
                # "hx-trigger":'keyup changed delay:500ms',
                # "hx-target":'#recipe-container',
                # "hx-swap": 'outerHTML'
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quanity', 'unit']