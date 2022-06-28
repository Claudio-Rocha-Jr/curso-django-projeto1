from django.urls import path

from . import views  # IMPORTING FROM RECIPES (.) LOCAL

#can use instead of name -- recipes:home
app_name = 'recipes'

urlpatterns = [
    path('', views.home, name="home"),
    path('recipes/category/<int:category_id>/', views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
]
