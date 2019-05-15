from django.urls import path
from . import views


app_name = 'turn'
urlpatterns = [

#for sicks
    path('list/', views.shift_list_for_sick, name='list'),
    path('<int:id>/set-turn/', views.set_turn_for_sick, name='set-turn'),
    path('passed/', views.passed_for_sick, name='passed'),
    path('load/', views.load_for_sick, name='load'),
    path('cash/increase', views.increase_cash_for_sick_list, name='cash-increase'),
    path('cash/increase/<int:amount>/', views.increase_cash_for_sick, name='cash-increase-amount'),
    path('cash/', views.cash_for_sick, name='sick-cash'),

#for doctors 
	path('my-shifts/', views.shift_list_for_doctor, name='doctor-shifts'),
	path('<int:id>/', views.take_visite, name='shift'),
	path('my-passed-turns/', views.passed_for_doctor, name='doctor-passed-turns'),
	path('my-cash-list/', views.cash_for_doctor, name='doctor-cashes'),

#for staff
	path('create/', views.create_shift, name='shift-create'),
	path('<int:id>/edit', views.edit_shift, name='shift-edit'),
	path('<int:id>/delete', views.delete_shift, name='shift-delete'),
	path('<int:id>/detail', views.detail_shift, name='shift-delete'),
	path('manage/', views.manage, name='shift-manage'),
	path('passed-shifts/', views.passed_shifts, name='shift-passed'),
]
