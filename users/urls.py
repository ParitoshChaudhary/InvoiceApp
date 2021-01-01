from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    register_view,
    login_view,
    logout_view,
    account_view,
    account_search_view,
    edit_account_view,
    get_all_users,
)

app_name = 'users'

urlpatterns = [
    path('search/', account_search_view, name="search"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_reset/password_change_done.html'),
         name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_reset/password_change.html'),
         name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
    path('<user_id>/', account_view, name='account_view'),
    path('<user_id>/edit/', edit_account_view, name='edit'),
    path('user_list', get_all_users, name='get_all_users')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
