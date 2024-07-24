from django import forms
from .models import Category, Tasks

class TaskCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False)

    class Meta:
        model = Tasks
        fields = ['title', 'description', 'priority',
                  'is_completed', 'deadline', 'category']
        
class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
