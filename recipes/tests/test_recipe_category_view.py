from unittest import skip

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


#@skip('Esse decorator pula o teste')
class RecipeCategoryViewTest(RecipeTestBase):

    # def tearDown(self) -> None:
    #     return super().tearDown()

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertIs(view.func.view_class,views.RecipeListViewCategory)

    def test_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertEqual(response.status_code,404)

    def test_recipe_cateogory_template_loads_recipes(self):
        needled_title = 'This is a category test'
        self.make_recipe(title=needled_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))

        self.assertEqual(len(response.context['recipes']), 1)
        response_context = response.content.decode('utf-8')

        self.assertIn(needled_title,response_context)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:category', kwargs = {'category_id' : recipe.category.id}))
        content = response.content.decode('utf-8')
        #response_context_recipes = response.context['recipes']

        self.assertEqual(response.status_code,404)

