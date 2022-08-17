# sobe o servidor porem sem aquivos staticos
from django.test import LiveServerTestCase

# sobe o servidor completo
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_chrome_browser
from recipes.tests.test_recipe_base import RecipeMixin

import time


class RecipesBaseFunctionTestCase(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, secs):
        time.sleep(secs)
