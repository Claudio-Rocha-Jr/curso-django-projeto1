from unittest import skip

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


#@skip('Esse decorator pula o teste')
class RecipeHomeViewTest(RecipeTestBase):

    # def tearDown(self) -> None:
    #     return super().tearDown()

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func,views.home)

    def test_recipe_home_view_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code,200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response,'recipes/pages/home.html')

    #@skip('WIP')
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
            )
        #Força o teste a falhar
        #self.fail('Para que eu termine de digitá-lo')

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe(author_data={
            'first_name':'Claudio'
            })
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(len(response.context['recipes']), 1)
        response_context = response.content.decode('utf-8')

        self.assertIn('Recipe Title',response_context)
        self.assertIn('5 Porções',response_context)
        self.assertIn('10 Minutos',response_context)
        self.assertIn('Claudio',response_context)
