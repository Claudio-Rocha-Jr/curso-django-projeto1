from unittest.mock import patch

from django.urls import reverse

from .test_recipe_base import RecipeTestBase


#@patch('recipes.views.PER_PAGE', new = 3)
class PaginationTest(RecipeTestBase):
    
    def test_if_total_qty_shown_in_template_matches_the_required(self):
        
        for i_recipe in range(12):
            self.make_recipe(
               slug = f'slug-{i_recipe}' ,
               title = f'titulo {i_recipe}',
               author_data = {'username':f'user{i_recipe}'}
            )

        with patch('recipes.views.PER_PAGE', new = 3):
            response = self.client.get(reverse('recipes:search') + f'?q=titulo')

        self.assertEquals(3,len(response.context['recipes']))
