
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.fast
@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep(15)
        self.assertIn('No recipes found here',body.text)
        
    @patch('recipes.views.PER_PAGE', new =9)
    def test_recipe_search_input_can_find_correct_recipe(self):
        recipes = self.make_recipe_in_batch(qtd=8)
        recipes[0].title = 'This is what I need'
        recipes[0].save()
        #User open the page
        self.browser.get(self.live_server_url)

        #User lookup for the text "Search for a recipe"

        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
        )

        #Click the input field and type the search term - Titulo 1
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.sleep(5)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(recipes[0].title,body.text)
        
    @patch('recipes.views.PER_PAGE', new =2)
    def test_recipe_home_page_pagination(self):

        #User opens the page
        self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        
        #Vê que tem uma paginação e clica pg 2

        page2 = self.browser.find_element(
            By.XPATH, 
            '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )

