from ast import Try
from cmath import exp
from curses.ascii import HT
from tokenize import group
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import request
from .forms import GroupForm, ExpenseForm, EditGroupForm, SettleTransactionsForm
from django.http import HttpResponse
from django.http import Http404
from django.views import generic
from .models import *
from django.contrib.auth.models import User
from .transaction_simplification import transaction_simplification


def get_user_grp(user,group_id):
    try:
        user_group = UserGroup.objects.get(id=group_id)
        if not user in user_group.users.all():
            raise Exception
        else:
            return user_group
    except Exception as e:
        print(e)
        raise Http404


@login_required
def home(request):
    return render(request, 'registration/success.html', {})


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
def user_group_list(request):
    all_groups = UserGroup.objects.all()
    logged_in_user = request.user
    logged_in_user_groups = []

    for group in all_groups:
        if logged_in_user in group.users.all():
            logged_in_user_groups.append(group)

    payload = {
        'groups': logged_in_user_groups
    }
    return render(request, 'groups/user_group_list.html', payload)


def add_member_to_grp(group_form):
    group_form.save(commit=False) # do not save the form data to database yet
    group = group_form.save()
    group_form.save_m2m() # save the form data to database

    group.users.add(request.user) # add user to database object instance
    group.save() # save the instance to database


def success_redirect(message):
    request.session['label'] = message
    request.session['create_redirect'] = 'True'
    return redirect('success')

@login_required
def create_group(request):
    if request.method == 'POST':
        group_form = GroupForm(request.POST) # create form with input data

        if group_form.is_valid(): # user input data is valid
            add_member_to_grp(group_form) # add user to database using data in form
            return success_redirect(f'Group {group.name} created')
        else: # for debugging
            print(group_form.errors)

    else:
        group_form = GroupForm() # create empty form

    return render(request, 'groups/create_group.html', {'form': group_form})


# @login_required
# def create_group(request):
#     group_form = GroupForm(request.POST or None)

#     if group_form.is_valid():
#         group_form.save(commit=False)
#         group = group_form.save()
#         group_form.save_m2m()
#         group.users.add(request.user)
#         group.save()
#     else:
#         print(group_form.errors)

#     group_context = { 'form': group_form }
    
#     if request.method == 'POST' and group_form.is_valid():
#         request.session['label'] = f'{group.name} created'
#         request.session['create_redirect'] = 'True'
#         return redirect('success')
#     else:
#         return render(request, 'groups/create_group.html', group_context)


@login_required
def success(request):
    if request.user.is_authenticated \
    and request.user.is_active:
        if 'create_redirect' in request.session \
        and 'label' in request.session:
            del request.session['create_redirect']
            return render(request, 'messages/success.html')
        else:
            raise Http404
    else:
        raise Http404


@login_required
def user_group_detail(request, group_id):
    group = get_user_grp(request.user, group_id)

    group_expenses = Expense.objects.filter(
        group__id=group_id,
        settled_expense=False)
    group_members = group.users.all()
    payload = {
        'group_id': group.id,
        'group_name': group.name,
        'expenses': group_expenses,
        'members': group_members
    }
    return render(request, 'groups/user_group_detail.html', payload)

def add_expense_to_grp(expense_form, group_id):
    user_group = get_user_grp(request.user, group_id)
    expense = expense_form.save(commit=False)
    expense.group = user_group
    expense_form.save()
    expense_form.save_m2m()
    return expense

@login_required
def add_expense(request, group_id):
    if request.method == 'POST': # submit the form
        expense_form = ExpenseForm(request.POST) # create form with the input details
        if expense_form.is_valid():
            expense = add_expense_to_grp(expense_form, group_id)
            return success_redirect(f'{expense.name} expense added')
        else:
            print(expense_form.errors)

    else: # fetch the form
        expense_form = ExpenseForm()

    return render(request, 'expense/add_expense.html', {'form': expense_form})



  

# @login_required
# def add_expense(request, group_id):
#     expense_form = ExpenseForm(request.POST or None)

#     if expense_form.is_valid():
#         try:
#             user_group = UserGroup.objects.get(id=group_id)
#             if not request.user in user_group.users.all():
#                 raise Exception
#         except Exception as e:
#             print(e)
#             raise Http404

#         expense = expense_form.save(commit=False)
#         expense.group = user_group
#         expense_form.save()
#         expense_form.save_m2m()
#     else:
#         print(expense_form.errors)

#     payload = { 'form': expense_form }

#     if request.method == 'POST' and expense_form.is_valid():
#         request.session['label'] = f'{expense.name} expense added'
#         request.session['create_redirect'] = 'True'
#         return redirect('success')
#     else:
#         return render(request, 'expense/add_expense.html', payload)


@login_required
def add_member(request, group_id):
    new_member_form = EditGroupForm(request.POST or None)
    new_member_form.fields['users'].queryset = User.objects.all()
    if new_member_form.is_valid():
        user_group = get_user_grp(request.user, group_id)
        user_group.users.add(*new_member_form.cleaned_data['users'])
        user_group.save()
    else:
        print('e')
        print(new_member_form.errors)

    payload = { 'form': new_member_form }
    
    if request.method == 'POST' and new_member_form.is_valid():
        label = 'Added '
        for member in new_member_form.cleaned_data['users']:
            label += member.username + '\n'
        request.session['label'] = label
        request.session['create_redirect'] = 'True'
        return redirect('success')
    else:
        return render(request, 'groups/add_member.html', payload)


@login_required
def view_unsettled_transactions(request, group_id):
    user_group = get_user_grp(request.user, group_id)

    all_transactions = Expense.objects.filter(group__id=user_group.id)
    unsettled_transactions = transaction_simplification(all_transactions)

    payload = {
        'unsettled_expenses': unsettled_transactions
    }
    return render(request, 'expense/unsettled_expenses.html', payload)

@login_required
def settle_expense(request, group_id, expense_id):
    user_group = get_user_grp(request.user, group_id)

    # change expense to true
    # add settlement