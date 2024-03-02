from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('edit-profile/',views.edit_profile,name='edit-profile'),
    path('settings/',views.settings,name='settings'),
    path('change-password',views.change_password,name='change-password'),
    path('delete-account',views.delete_account,name='delete-account'),
    path('verify/<str:verification_code>/', views.verify_email, name='verify_email'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<str:forgot_password_token>/', views.reset_password, name='reset-password'),

]
