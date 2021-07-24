from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout_page'),
    path('new-post/', views.new_post, name='new_post')
]
