from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', view=views.user_login, name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('manager-dashboard/', view=views.power_user_dashboard, name='power_user_dashboard'),
    path('edit-profile/<uuid:profile_id>/', views.edit_profile, name='edit_profile'),
    path('create_user/', view=views.create_user_department_profile, name='create_user'),
    path('create_company/', view=views.company_signup, name='company_signup'),
]
