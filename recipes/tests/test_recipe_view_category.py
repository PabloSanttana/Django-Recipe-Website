
from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase

# from unittest import skip # usando para pular teste @skip
# TESTE PARA FUNÇÕES DA views

# ---------------------------Category---------------------------------------------


class RecipeViewCategoryTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1000})
        view = resolve(url)
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_404_if_no_recieps_found(self):
        url = reverse('recipes:category', kwargs={'category_id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_loads_correct_template(self):
        recipe = self.make_recipe()
        url = reverse('recipes:category', kwargs={
                      'category_id': recipe.category.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_recipe_category_template_loads_recipe(self):
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
        url = reverse('recipes:category', kwargs={
                      'category_id': recipe.category.id})
        response = self.client.get(url)
        # response_recipes = response.context['recipes'].first()
        # self.assertEqual(response_recipes.title, 'title')
        content = response.content.decode('utf-8')
        self.assertIn('title', content)
        self.assertIn('first_name last_name', content)
        self.assertIn('Carnes', content)

    def test_recipe_category_template_dont_loads_recipes_not_published(self):
        """Test recipes is_published False not Show"""
        recipe = self.make_recipe(is_published=False)
        url = reverse('recipes:category', kwargs={
                      'category_id': recipe.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
