from django.urls import path
from . import views
from .views import user_list


urlpatterns = [


path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
path('user-list/', user_list, name='user_list'),
path('user_details/<int:user_id>/', views.user_details, name='user_details'),
path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
path('question-delete/<int:pk>/',views.delete_question, name='delete_question'),


]
