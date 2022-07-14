from unittest import skip

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


#@skip('Esse decorator pula o teste')
class RecipeDetailViewTest(RecipeTestBase):

    # def tearDown(self) -> None:
    #     return super().tearDown()

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id':1}))
        self.assertIs(view.func,views.recipe)


    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1000}))
        self.assertEqual(response.status_code,404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needled_title = 'This is a detail page - It loads one recipe'
        self.make_recipe(title=needled_title)
        response = self.client.get(reverse('recipes:recipe', kwargs = {'id' : 1}))

        content = response.content.decode('utf-8')

        self.assertIn(needled_title,content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs = {'id' : recipe.id}))
        content = response.content.decode('utf-8')
        #response_context_recipes = response.context['recipes']

        self.assertEqual(response.status_code,404)

