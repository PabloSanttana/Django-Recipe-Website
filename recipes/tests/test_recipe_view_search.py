
from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase

# from unittest import skip # usando para pular teste @skip
# TESTE PARA FUNÇÕES DA views


class RecipeViewSearchTest(RecipeTestBase):

    def test_recipe_search_uses_correct_view_funcion(self):
        url = reverse('recipes:search')
        view = resolve(url)
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_corret_template(self):
        url = reverse('recipes:search') + '?search=Receita'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/recipe-search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_is_no_page_escaped(self):
        url = reverse('recipes:search') + '?search=<Receita>'
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn('&lt;Receita&gt', content)

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'
        recipe1 = self.make_recipe(
            author_data={
                'username': "one",
            },
            title=title1,
            slug="slug-1"
        )
        recipe2 = self.make_recipe(
            author_data={
                'username': "Two",
            },
            title=title2,
            slug="slug-2"
        )
        url = reverse('recipes:search')
        response1 = self.client.get(f'{url}?search={title1}')
        response2 = self.client.get(f'{url}?search={title2}')
        response3 = self.client.get(f'{url}?search=this')
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response3.context['recipes'])
        self.assertIn(recipe2, response3.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):

        recipe = self.make_recipe(
            category_data={'title': 'Carnes'},
            title="Carnes Vovó",
            description="Mais uma receita delicia de cozidas"
        )
        url = reverse('recipes:search') + '?search=delicia'
        response = self.client.get(url)
        self.assertIn(recipe, response.context['recipes'])
