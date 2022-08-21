from django.urls import path

from . import views

# recipes:recipe
# from recipes.views import home
app_name = 'recipes'

urlpatterns = [
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path("recipes/search/", views.RecipeListViewSearch.as_view(), name="search"),
    path("recipes/category/<int:category_id>/",
         views.RecipeListViewCategory.as_view(), name="category"),
    path("recipes/<slug:slug>/", views.RecipeDetailView.as_view(), name="recipe"),


]
