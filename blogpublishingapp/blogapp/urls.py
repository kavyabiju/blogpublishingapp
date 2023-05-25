from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('user_home', views.user_home, name="user_home"),

    path('add_blog', views.add_blog, name='add_blog'),
    path('see_blog', views.see_blog, name='see_blog'),
    path('logout-view/', views.logout_view, name="logout_view"),
    path('register', views.register_view, name="register_view"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('admin_main', views.admin_main, name="admin_main"),
    path('blog_details/<slug>', views.blog_detail, name='blog_detail'),
    path('blog_update/<slug>/', views.blog_update, name="blog_update"),
    path('rate',views.rate,name="rate"),
    path('blog_delete/<id>', views.blog_delete, name="blog_delete"),
    path('profile', views.profile, name="profile"),
    path('draft', views.draft1, name='draft'),
    path('blog_edit/<slug>/', views.blog_edit, name="blog_edit"),
    path('draft_update/<slug>/', views.draft_update, name="draft_update"),
    path('draf_delete/<id>', views.draft_delete, name="draft_delete"),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('search', views.search, name="search"),
    
]
