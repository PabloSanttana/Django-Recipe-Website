from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase
# ---------------------------detail---------------------------------------------


class RecipeViewDetailTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'slug': 'Receita-35'})
        view = resolve(url)
        # Baseado em def
        # self.assertIs(view.func., views.function)
        # Baseado em class
        self.assertIs(view.func.view_class, views.RecipeDetailView)

    def test_recipe_detail_view_404_if_no_recieps_found(self):
        url = reverse('recipes:recipe', kwargs={'slug': 'Receita-35'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_loads_correct_template(self):
        recipe = self.make_recipe()
        url = reverse('recipes:recipe', kwargs={'slug': recipe.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')

    def test_recipe_detail_template_loads_recipe(self):
        # criando receitas
        recipe = self.make_recipe(author_data={
            'username': "username",
            'first_name': "first_name",
            'last_name': 'last_name',
            'email': "user@example.com",
            'password': "password"
        },
            category_data={'title': 'Carnes'}
        )
        url = reverse('recipes:recipe', kwargs={'slug': recipe.slug})
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn('title', content)
        self.assertIn('first_name last_name', content)
        self.assertIn('Carnes', content)

    def test_recipe_detail_template_dont_loads_recipes_not_published(self):
        """Test recipes is_published False not Show"""
        recipe = self.make_recipe(is_published=False)
        url = reverse('recipes:recipe', kwargs={'slug': recipe.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
