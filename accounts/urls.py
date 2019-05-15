from django.urls import path
from . import views

#from posts import views as ...
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_function, name='login'),
    path('logout/', views.logout_function, name='logout'),
    path('signup/doctor', views.signup_doctor_function, name='signup-doctor'),
    path('signup/sick', views.signup_sick_function, name='signup-sick'),
    path('account', views.account, name='account'),
    path('account/edit', views.edit, name='edit'),

    path('doctor-manage', views.doctor_management, name='doctor-manage'),
    path('doctor-manage/<int:id>/delete', views.doctor_delete, name='doctor-delete'),
    path('doctor-cash-list', views.doctor_cash_list, name='doctor-cash-list'),

    path('sick-manage', views.sick_management, name='sick-manage'),
    path('sick-manage/<int:id>/delete', views.sick_delete, name='sick-delete'),
    path('sick-cash-list', views.sick_cash_list, name='sick-cash-list'),

    path('', views.home, name='home'),
]
