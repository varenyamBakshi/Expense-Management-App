"""expense_management_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_group_list, name='user_group_list_1'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('groups/', views.user_group_list, name='user_group_list'),
    path('groups/success/', views.create_group_success, name='create_group_success'),
    path('group/<int:pk>/`', views.UserGroupDetailView.as_view(), name='group_detail'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('create_group/', views.create_group, name='create_group'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_member/', views.add_member, name='add_member'),
    path('view_unsettled_transactions/<int:id>/', views.view_unsettled_transactions, name='view_unsettled_transactions'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
