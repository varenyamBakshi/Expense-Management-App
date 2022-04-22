from django import forms
from .models import UserGroup
  
  
class GroupForm(forms.ModelForm):
  
    class Meta:
        model = UserGroup
  
        fields = [
            'users',
            'name'
        ]