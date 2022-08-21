
from .RecipeListViewBase import RecipeListViewBase
from django.views.generic import DetailView
from django.db.models import Q
from django.http import Http404
from recipes.models import Recipe


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id'),
        )
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        recipe = ctx.get('recipes')
        ctx.update(
            {'title': f'{recipe[0].category.title} - category'}

        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/recipe-search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('search', '').strip()
        if not search_term:
            raise Http404

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('search', '').strip()
        ctx.update(
            {'search': search_term, 'additional_url_query': f'&search={search_term}'}

        )
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(slug=slug, is_published=True)
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {
                "is_detail_page": True
            }

        )
        return ctx
