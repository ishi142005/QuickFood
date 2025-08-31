from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-recipes/', views.get_recipes, name='get_recipes'),
    path('add-to-pantry/', views.add_to_pantry, name='add_to_pantry'),
    path('remove-from-pantry/', views.remove_from_pantry, name='remove_from_pantry'),
    path('clear-pantry/', views.clear_pantry, name='clear_pantry'),
    path('upload/', views.upload_ingredient, name='upload_ingredient'),
]
