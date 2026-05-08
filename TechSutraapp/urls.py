from django.urls import path
from TechSutraapp.views import home, view, dashboard, login_view, register, resources, logout_view, resource_list, about, platform_reviews

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('reviews/', platform_reviews, name='reviews'),
    path('home/', home, name='home_alt'),
    path('view/', view, name='view'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('resources/<int:subject_id>/', resources, name='resources'),
    path('resources/<int:subject_id>/<str:resource_type>/', resource_list, name='resource_list')
]