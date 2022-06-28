
from django.http import Http404
from django.shortcuts import render
from utils.recipes.factory import make_recipe

from recipes.models import Recipe


# Create your views here.
def home(request):
    recipes = Recipe.objects.all().filter(is_published = True).order_by('-id')
    return render(request,'recipes/pages/home.html', context = {
        'recipes':recipes,
        'page_title':'Home'
    })

def recipe(request, id):
    return render(request,'recipes/pages/recipe-view.html', context = {
        'recipe':Recipe.objects.filter(id = id).order_by('-id'),
        'is_detail_page':True,
    })

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id = category_id,is_published = True).order_by('-id')

    if not recipes:
        raise Http404('Not found')

    return render(request,'recipes/pages/home.html', context = {
        'recipes':recipes,
        'page_title':f'{recipes.first().category.name} - Category'})
