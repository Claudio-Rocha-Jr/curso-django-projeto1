from django.urls import reverse

from .test_recipe_base import RecipeTestBase


class PaginationTest(RecipeTestBase):
    
    def test_if_total_qty_shown_in_template_matches_the_required(self):
        
        for i_recipe in range(12):
            self.make_recipe(
               slug = f'slug-{i_recipe}' ,
               title = f'titulo {i_recipe}',
               author_data = {'username':f'user{i_recipe}'}
            )

        response = self.client.get(reverse('recipes:search') + f'?q=titulo')

        self.assertEquals(9,len(response.context['recipes']))
