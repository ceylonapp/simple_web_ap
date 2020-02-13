from django.urls import path

from . import views

urlpatterns = [
    # Without Login Views
    path('', views.home_page, name='index_page'),
    path('faq', views.faq_view, name='faq_view'),
    path('guideline', views.guideline_view, name='guideline_view'),
    path('login', views.login_page, name='login_page'),
    # Without Login Actions
    path('create_account', views.create_account, name='create_account_action'),
    # If logged in then show users details otherwise users posts
    path('user/<str:username>', views.user_profile, name='view_user_profile'),

    path('password_reset', views.forgot_password_page, name='forgot_password_page'),
    path('password_reset_complete', views.password_reset_complete_view, name='password_reset_complete'),
    path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('post', views.submit_task, name='submit_task'),

]
