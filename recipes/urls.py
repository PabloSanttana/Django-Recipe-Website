from django.urls import path

from . import views

# recipes:recipe
# from recipes.views import home
app_name = 'recipes'

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/search/", views.search, name="search"),
    path("recipes/category/<int:category_id>/",
         views.category, name="category"),
    path("recipes/<slug:slug>/", views.recipe, name="recipe"),


]
