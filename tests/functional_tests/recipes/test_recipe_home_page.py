from .base import RecipesBaseFunctionTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class RecipeHomeFunctionalTest(RecipesBaseFunctionTestCase):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        title_needed = "Nova Receita de Carnes"
        recipes[0].title = title_needed
        recipes[0].save()
        # Usuário abre a página
        self.browser.get(self.live_server_url)
        # ver um campo de buscar
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Buscar receitas..."]')

        # clicar no input e digita o termo de buscar "Recipe Title 1"
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        # verificando receita buscada correta
        title = self.browser.find_element(By.CLASS_NAME, "recipe-title")
        self.assertIn(title_needed, title.text)

    def test_recipe_navigation_pages(self):
        self.make_recipe_in_batch()
        # Usuário abre a página
        self.browser.get(self.live_server_url)
        # ver um campo de navegation, seleciona page 2
        page2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]')
        # enter page 2
        page2.click()
        # ver a pagina 2
        # verificando se estou na pagina 2 e quantos receitas tem
        current_page = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Current page, 2"]')
        recipes = self.browser.find_elements(By.CLASS_NAME, 'recipe-list-item')
        self.assertIn('2', current_page.text)
        self.assertEqual(9, len(recipes))
