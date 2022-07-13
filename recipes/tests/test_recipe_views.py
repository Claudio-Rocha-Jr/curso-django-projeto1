from unittest import skip

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


#@skip('Esse decorator pula o teste')
class RecipeViewsTest(RecipeTestBase):

    # def tearDown(self) -> None:
    #     return super().tearDown()

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func,views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertIs(view.func,views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id':1}))
        self.assertIs(view.func,views.recipe)

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

    def test_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertEqual(response.status_code,404)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1000}))
        self.assertEqual(response.status_code,404)

    def test_recipe_cateogory_template_loads_recipes(self):
        needled_title = 'This is a category test'
        self.make_recipe(title=needled_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))

        self.assertEqual(len(response.context['recipes']), 1)
        response_context = response.content.decode('utf-8')

        self.assertIn(needled_title,response_context)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needled_title = 'This is a detail page - It loads one recipe'
        self.make_recipe(title=needled_title)
        response = self.client.get(reverse('recipes:recipe', kwargs = {'id' : 1}))

        content = response.content.decode('utf-8')

        self.assertIn(needled_title,content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        #response_context_recipes = response.context['recipes']

        self.assertIn('<h1>No recipes found here</h1>',content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:category', kwargs = {'category_id' : recipe.category.id}))
        content = response.content.decode('utf-8')
        #response_context_recipes = response.context['recipes']

        self.assertEqual(response.status_code,404)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs = {'id' : recipe.id}))
        content = response.content.decode('utf-8')
        #response_context_recipes = response.context['recipes']

        self.assertEqual(response.status_code,404)
