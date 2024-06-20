"""
URL configuration for search_jobs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from webapp import views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.myapp, name='login'),
    path('sign-up', views.signup, name='signup'),
    path('login', views.signup_info, name='signup_inf'),
    path('dash', views.login_info, name='login_inf'),
    path('forget-password', views.forget, name='forget_pass'),
    path('verify-code', views.verify, name='verify-pass'),
    path('verification-code', views.email_verify, name='code'),
    path('enter-code', views.code_verify, name='code-enter'),
    path('changed', views.update_pass, name='update-pass'),
    path('client-page', views.client_dashboard, name='client'),
    path('internships', views.save_internship, name='interns'),
    path('api/items/', views.get_items, name='get_items'),
    path('api/items/<str:item_id>/', views.get_item, name='get_item'),
    path('api/items/create/', views.create_item, name='create_item'),
    path('client-postings', views.cli_dash, name='cli-postings'),
    path('intern-list', views.interns_list, name='int_list'),
    path('profile', views.profile, name='profile'),
    path('save-tag', views.save_tags, name='tags'),
    path('dash-applied', views.applied, name='apply'),
]