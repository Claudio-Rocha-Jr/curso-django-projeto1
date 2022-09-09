
import os

#from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, ListView
from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe

from recipes.models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, context.get('recipes'), PER_PAGE)
        context.update(
            { 'recipes': page_obj, 'pagination_range': pagination_range}
            )
        return context

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id = self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'page_title':f'{context.get("recipes")[0].category.name} - Category'
            })
        return context

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self,*args, **kwargs):
        search_term = self.request.GET.get('q','').strip()

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(title__icontains=search_term) | #contains i for not case sensitive
            Q(description__icontains=search_term),
            is_published = True
    ).order_by('-id')
        return qs
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q','').strip()

        context.update({
            'page_title' : f'Search for "{search_term}"',
            'search_term': search_term,
            'additional_url_query':f'&q={search_term}'
            })
        return context
        


# Create your views here.
def home(request):

    recipes = Recipe.objects.all().filter(is_published = True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request,'recipes/pages/home.html', context = {
        'recipes':page_obj,
        'page_title':'Home',
        'pagination_range':pagination_range
    })

def category(request, category_id):
    # recipes = Recipe.objects.filter(category__id = category_id,is_published = True).order_by('-id')

    # if not recipes:
    #     raise Http404('Not found')
    #category__id is the id column of the related category table
    recipes = get_list_or_404(Recipe.objects.filter(category__id = category_id,is_published = True).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request,'recipes/pages/home.html', context = {
        'recipes':page_obj,
        'pagination_range':pagination_range,
        'page_title':f'{recipes[0].category.name} - Category'})


def recipe(request, id):
    #recipe = Recipe.objects.filter(id = id).order_by('-id').first()

    recipe = get_object_or_404(Recipe, id = id, is_published = True)

    return render(request,'recipes/pages/recipe-view.html', context = {
        'recipe':recipe,
        'is_detail_page':True,
    })

def search(request):
    
    search_term = request.GET.get('q','').strip()

    if not search_term:
        raise Http404

    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) | #contains i for not case sensitive
        Q(description__icontains=search_term),
        is_published = True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title' : f'Search for "{search_term}"',
        'search_term': search_term,
        'recipes':page_obj,
        'pagination_range':pagination_range,
        'additional_url_query':f'&q={search_term}'
    })

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self,*args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page' : True
        })

        return ctx
