
from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch  # manipular variaveis de ambiente para os teste

# from unittest import skip # usando para pular teste @skip
# TESTE PARA FUNÇÕES DA views


class RecipeViewsTest(RecipeTestBase):

    # def tearDown(self) -> None:
    #    return super().tearDown()
    # -------------------------HOME-----------------------------------------

    def test_recipe_home_view_function_is_correct(self):
        url = reverse('recipes:home')
        view = resolve(url)
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_view_returns_status_200_ok(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # @skip("Progress") #pular o teste
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):

        url = reverse('recipes:home')
        response = self.client.get(url)
        # encontrar algo no texto HTML
        self.assertIn('No recipes found here',
                      response.content.decode('utf-8'))

        # tenho que escrever mais algumas coisas sobre o test
        # self.fail("Revisar test")

    def test_recipe_home_template_loads_recipes(self):
        # criando receitas
        self.make_recipe(author_data={
            'username': "username",
            'first_name': "first_name",
            'last_name': 'last_name',
            'email': "user@example.com",
            'password': "password"
        },
            category_data={'title': 'Carnes'}
        )
        url = reverse('recipes:home')
        response = self.client.get(url)
        # response_recipes = response.context['recipes'].first()
        # self.assertEqual(response_recipes.title, 'title')
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn('title', content)
        self.assertIn('first_name last_name', content)
        self.assertIn('Carnes', content)
        self.assertEqual(len(recipes), 1)

    def test_recipe_home_template_dont_loads_recipes_not_published(self):
        """Test recipes is_published False not Show"""
        self.make_recipe(is_published=False)
        url = reverse('recipes:home')
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn('No recipes found here', content)
        self.assertEqual(len(recipes), 0)

    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipe_home_template_shows_recipes_is_pagination(self):
        self.make_recipe_in_batch()
        url = reverse('recipes:home')
        response = self.client.get(url)
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 9)
        self.assertEqual(len(paginator.get_page(2)), 9)
        self.assertEqual(len(paginator.get_page(3)), 2)
