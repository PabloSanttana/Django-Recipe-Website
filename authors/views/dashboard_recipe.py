from django.views import View
from recipes.models import Recipe
from authors.forms import RecipeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class DashboardMixin:
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = get_object_or_404(
                Recipe, pk=id, is_published=False, author=self.request.user)

        return recipe

    def render_recipe(self, form, title, template):
        return render(self.request, template, context={
            'form': form,
            'title': title
        })

    def recipe_save(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        return recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name="dispatch"
)
class DashboardRecipe(View, DashboardMixin):

    def __init__(self, *args, **kwargs):
        # sobre escrevendo metodos
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        # sobre escrevendo metodos
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        # sobre escrevendo metodos
        return super().dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('id', None))
        form = RecipeForm(instance=recipe)
        return self.render_recipe(form=form,
                                  title="Dashboard Recipe",
                                  template='authors/pages/dashboard_recipes.html'
                                  )

    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
        if form.is_valid():
            recipe = self.recipe_save(form)
            messages.success(request, 'Save with success.')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

        return self.render_recipe(form=form,
                                  title='Dashboard Recipe',
                                  template='authors/pages/dashboard_recipes.html'
                                  )


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name="dispatch"
)
class DashboardRecipeDelete(View, DashboardMixin):
    def post(self, *args, **kwargs):
        id = self.request.POST.get('id')
        recipe = self.get_recipe(id)
        recipe.delete()
        messages.success(self.request, 'Delete with success.')
        return redirect('authors:dashboard')
