from ast import Try
from tokenize import group
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GroupForm
from django.http import HttpResponse
from django.http import Http404
from django.views import generic
from .models import *

class UserGroupListView(generic.ListView):
    model = UserGroup
    template_name = 'expense/usergroup_list.html'

class UserGroupDetailView(generic.DetailView):
    model = UserGroup
    template_name = "expense/usergroup_detail.html"
    

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