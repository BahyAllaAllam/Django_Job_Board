from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/edit/email', views.change_email, name='change_email'),
    path('user/<int:id>/delete', views.delete_user, name='delete-user'),

]

