from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.models import Page
from wagtail.search.models import Query

from recipes.models import RecipePage
from home.models import GeneralSettings


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    if search_query:
        search_results = RecipePage.objects.live().search(search_query)
        query = Query.get(search_query)
        query.add_hit()
    else:
        search_results = Page.objects.none()

    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })


def random(request):
    """
    Get a random recipe to make for dinner
    """
    random_recipe_category = GeneralSettings.for_request(request).random_recipe_category
    if random_recipe_category:
        random_recipe = random_recipe_category.get_recipes().order_by('?').first()
    else:
        random_recipe = RecipePage.objects.live().order_by('?').first()

    return render(request, 'search/random.html', {
        'random_recipe': random_recipe,
    })
