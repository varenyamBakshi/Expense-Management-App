from django import forms
from .models import UserGroup, Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserModel
from django.contrib.auth.models import User
  
  
class GroupForm(forms.ModelForm):
  
    class Meta:
        model = UserGroup
        fields = ['name']


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = [
            'name',
            'amount',
            'payer',
            'users_involved'
        ]

class EditGroupForm(forms.ModelForm):
  
    class Meta:
        model = UserGroup
        fields = ['users']

class SettleTransactionsForm(forms.Form):
    file = forms.FileField()