from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.loginpage, name='loginpage'),
    path('register/',views.registerpage, name='registerpage'),
    path('user-Save',views.register_save,name='register_save'),
    path('user-login/',views.userlogin, name='userlogin'),
    path('logout/',views.userlogout, name='userlogout'),
    path('admin-logout/',views.admin_logout, name='admin_logout'),
    path('home/',views.index, name='index'),
    path('save-question/',views.askquestion,name='askquestion'),
    path('submit-answer/<int:pk>/',views.submit_answer,name='submit_answer'),
    path('view-answers/<int:pk>/',views.view_answers,name='view_answers'),
    path('like-answer/<int:answer_id>/',views.like_answer,name='like_answer'),
    path('profilepage',views.profilepage, name='profilepage'),
    path('edit-profile',views.edit_profile, name='edit_profile'),
    path('profile-save',views.edit_profile_save, name='edit_profile_save'),
    path('filter-today',views.filter_today, name='filter_today'),
    path('filter-myposts',views.filter_myposts, name='filter_myposts'),
    path('post-delete/<int:pk>/',views.delete_post, name='delete_post'),
    path('post-edit/<int:pk>/',views.edit_post, name='edit_post'),
    path('notifications/',views.notifications, name='notifications'),



]
