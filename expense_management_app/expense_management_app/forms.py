from django import forms
from .models import UserGroup, Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserModel
  
  
class GroupForm(forms.ModelForm):
  
    class Meta:
        model = UserGroup
  
        fields = [
            # 'users',
            'name'
        ]

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            'users_involved',
            'amount',
            'payer'
        ]

class MemberForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=UserModel.objects.all())