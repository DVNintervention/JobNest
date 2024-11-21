from django.urls import path
from . import views
from .views import UserLoginView

urlpatterns = [
    path('', views.landing_view, name='landing_page'),
    path('index/', views.index, name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('job-creation/',views.job_creation, name='job_creation'),
    path('accounts/profile/',views.profile_view, name='profile'),
    path('update-resume/', views.update_resume, name='update_resume'),
    path('edit_field/<str:field_name>/', views.edit_field_view, name='edit-field'),
    path('register/', views.register, name='register' ),
    path('register/register-type/', views.register_type, name='register_type' ),
    path('register/register-type/register-company/', views.register_company, name='register_company' ),
    path('register/register-type/register-user/', views.register_user, name='register_user'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:user_id>/', views.display_profile, name='display_profile'),
    path('dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('job-posting/<int:posting_id>/', views.job_posting_detail, name='job_posting_detail'),
    path('edit-field/<str:field_name>/', views.edit_field_view, name='edit-field'),
    path('chats/', views.list_chats, name='list_chats'),
    path('chat/<int:chat_id>/', views.view_chat, name='view_chat'),
    path('chat/<int:chat_id>/send-message/', views.send_message, name='send_message'),
    path('start-chat-with-jobseeker/<int:job_application_id>/', views.start_chat_with_jobseeker, name='start_chat_with_jobseeker'),
    path('job-map/', views.job_map, name='job_map'),
    path('apply-to-job/<int:posting_id>/', views.apply_to_job, name='apply_to_job'),
    path('update-application-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
]


