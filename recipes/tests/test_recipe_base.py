from django.test import TestCase

from recipes.models import Recipe, Category
from django.contrib.auth.models import User


class RecipeMixin:
    def make_category(self, title='Carnes'):
        return Category.objects.create(title=title)

    def make_author(self,
                    username="username",
                    first_name="first_name",
                    last_name='last_name',
                    email="user@example.com",
                    password="password"
                    ):
        return User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

    def make_recipe(self,
                    title="title",
                    description="description",
                    preparation_time=30,
                    preparation_time_unit='Minutos',
                    servings=5,
                    servings_unit="servings_unit",
                    preparation_steps="preparation_steps",
                    author_data=None,
                    category_data=None,
                    slug="recipe-slug",
                    preparation_steps_is_html=False,
                    is_published=True,
                    ):

        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return Recipe.objects.create(
            title=title,
            description=description,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            author=self.make_author(**author_data),
            category=self.make_category(**category_data),
            slug=slug,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qtd=20):
        recipes = []
        for i in range(qtd):
            kwargs = {
                'title': f'Recipe Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'r{i}'}

            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
