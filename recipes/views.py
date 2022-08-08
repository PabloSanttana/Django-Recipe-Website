from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q


# Create your views here.
from recipes.models import Recipe
from utils.pagnation import make_pagination


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    # recipes = get_list_or_404(Recipe.objects.filter(
    #    is_published=True).order_by('-id'))
    page_obj, pagination_range = make_pagination(request, recipes, 9, 4)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    # recipes = Recipe.objects.filter(
    #      category__id=category_id, is_published=True).order_by('-id')
    #  if not recipes
    #     raise http404('not found')

    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.title} - category'
    })


def recipe(request, slug):
    # recipe = Recipe.objects.filter(id=id).first()
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        "is_detail_page": True
    })


def search(request):
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        raise Http404
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')

    return render(request, 'recipes/pages/recipe-search.html', context={
        'recipes': recipes,
        'search': search_term,
    })
