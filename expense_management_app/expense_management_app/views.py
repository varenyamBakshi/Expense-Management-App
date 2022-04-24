from ast import Try
from curses.ascii import HT
from tokenize import group
from django.http import Http404, HttpResponseRedirect
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
class UserGroupDetailView(generic.DetailView):
    model = UserGroup
    template_name = 'groups/usergroup_detail.html'

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


@login_required
def create_group(request):
    group_form = GroupForm(request.POST or None)

    if group_form.is_valid():
        print('valid')
        group_form.save(commit=False)
        group = group_form.save()
        group_form.save_m2m()
        group.users.add(request.user)
        group.save()

    group_context = { 'form': group_form }
    
    if request.method == 'POST' and group_form.is_valid():
        request.session['group'] = group.name
        request.session['create_group_redirect'] = 'True'
        return redirect('create_group_success')
    else:
        return render(request, 'groups/create_group.html', group_context)


@login_required
def create_group_success(request):
    if request.user.is_authenticated \
    and request.user.is_active:
        if 'create_group_redirect' in request.session \
        and 'group' in request.session:
            del request.session['create_group_redirect']
            return render(request, 'groups/success.html')
        else:
            raise Http404
    else:
        raise Http404

@login_required()
def reciva(request):
    if request.user.is_authenticated() and request.user.is_active:
        if 'pp_redarekt' in request.session:
            execute(request)
            del request.session['pp_redarekt']
        raise Http404
    raise Http404

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
        return Http404('Group does not exist')
    print(request.user.id)
    return HttpResponse({'hi': 'hi'})