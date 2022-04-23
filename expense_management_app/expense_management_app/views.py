from ast import Try
from tokenize import group
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GroupForm, ExpenseForm, MemberForm
from django.http import HttpResponse
from django.http import Http404
from django.views import generic
from .models import *

@method_decorator(login_required, name='dispatch')
class UserGroupListView(generic.ListView):
    model = UserGroup
    template_name = 'groups/usergroup_list.html'

@method_decorator(login_required, name='dispatch')
class UserGroupDetailView(generic.DetailView):
    model = UserGroup
    template_name = "groups/usergroup_detail.html"

@login_required
def home(request):
    return render(request, "registration/success.html", {})

def register(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_group(request):
    group_form = GroupForm(request.POST or None)

    if group_form.is_valid():
        group_form.save(commit=False)
        group_form.save()
        group_form.save_m2m()

    group_context = { 'form': group_form }
    return render(request, 'groups/create_group.html', group_context)

@login_required
def add_expense(request):
    expense_form = ExpenseForm(request.POST or None)

    if expense_form.is_valid():
        expense_form.save(commit=False)
        expense_form.save()
        expense_form.save_m2m()

    expense_context = { 'form': expense_form }
    return render(request, 'expense/add_expense.html', expense_context)

@login_required
def add_member(request):
    member_form = MemberForm(request.POST or None)

    if member_form.is_valid():
        member_form.save(commit=False)
        member_form.save()
        member_form.save_m2m()

    member_context = { 'form': member_form }
    print(member_context)
    return render(request, 'groups/add_member.html', member_context)

@login_required
def view_unsettled_transactions(request, id):
    # if user in group:
    # do op
    # else 404
    try:
        group_obj = UserGroup.objects.get(id=id)
    except Exception as e:
        print(e)
        return Http404("Group does not exist")
    print(request.user.id)
    return HttpResponse({'hi': 'hi'})