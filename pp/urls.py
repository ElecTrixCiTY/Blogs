from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('fashion/', views.fashion_page, name='fashion'),
    path('photography/', views.photography_page, name='photography'),
    path('single/', views.single_page, name='single'),
    path('travel/', views.travel_page, name='travel'),
    path('register/', views.signup, name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.custom_logout, name='logout'),
    path('gallery/', views.gallery_page, name='gallery'),

    path('password_change/', views.password_change, name='password_change'),

    path('password_reset/', views.password_reset, name='password_reset'),
    
    path('reset/<uidb64>/<token>', views.password_reset_confirm,
         name='password_reset_confirm'),    

    

    
]

