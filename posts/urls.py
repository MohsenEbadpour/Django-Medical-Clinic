from django.urls import path
from . import views

# from posts import views as ...
app_name = 'posts'
urlpatterns = [
	path('create/', views.post_create, name='create'),
	path('<int:id>/', views.post_detail, name='detail'),
	path('<int:id>/edit', views.post_edit, name='edit'),
	path('<int:id>/delete', views.post_delete, name='delete'),
	path('archives/', views.post_archives, name='archives')
	]
