
from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


# testenado os Models de recipes


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category()
        return super().setUp()

    def test_recipe_category_filds_max_length(self):
        # faz a mudaça do category.title
        self.category.title = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_recipes_category_string_representation(self):
        self.category.title = 'Testing Representation'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), 'Testing Representation')
