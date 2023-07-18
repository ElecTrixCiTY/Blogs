from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
 
    path('register/', views.signup, name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.custom_logout, name='logout'),
    path('gallery/', views.gallery_page, name='gallery'),

    path('blogs/', views.blog_page, name='blogs'),
    path('add-blog/', views.add_blog, name="add_blog"),
    path('blog-detail/<slug>', views.blog_detail, name='blog_detail'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('blog-delete/<id>', views.blog_delete, name = 'blog_delete'),
    path('blog_update/<slug>', views.blog_update, name='blog_update'),

    path('password_change/', views.password_change, name='password_change'),

    path('password_reset/', views.password_reset, name='password_reset'),
    
    path('reset/<uidb64>/<token>', views.password_reset_confirm,
         name='password_reset_confirm'),    

    

    
]

