from datetime import date

from django.core.management import call_command
from django.test import TestCase, RequestFactory

from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Page, Site

from images.models import CustomImage
from recipes.models import RecipePage, RecipeIndexPage
from search.views import search


def make_test_image():
    image = CustomImage(title="Test image", file=get_test_image_file())
    image.save()
    return image


class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Use existing root page from initial migrations
        root_page = Page.objects.get(depth=1)

        # Create a test home page under root with a unique slug
        test_home = Page(title="Test Home", slug="test-search-home")
        root_page.add_child(instance=test_home)
        Site.objects.create(
            hostname="search-test.localhost",
            root_page=test_home,
            is_default_site=False,
        )

        recipe_index = RecipeIndexPage(title="Test Recipes", slug="test-recipes")
        test_home.add_child(instance=recipe_index)

        image = make_test_image()

        cls.cookie_recipe = RecipePage(
            title="Chocolate Chip Cookies",
            slug="test-chocolate-chip-cookies",
            intro="Classic cookies with chocolate chips.",
            ingredients="2 cups flour\n1 cup butter\n2 cups chocolate chips\n1 cup sugar",
            instructions="Mix butter and sugar. Add flour. Fold in chocolate chips. Bake at 375 for 10 minutes.",
            post_date=date.today(),
            live=True,
            main_image=image,
        )
        recipe_index.add_child(instance=cls.cookie_recipe)

        cls.soup_recipe = RecipePage(
            title="Tomato Soup",
            slug="test-tomato-soup",
            intro="A rich tomato soup.",
            ingredients="4 tomatoes\n1 onion\n2 cloves garlic",
            instructions="Saute onion and garlic. Add tomatoes. Simmer 20 minutes. Blend.",
            post_date=date.today(),
            live=True,
            main_image=image,
        )
        recipe_index.add_child(instance=cls.soup_recipe)

        # Populate the search index — required after loading data into a fresh
        # database. The database search backend does not auto-index on creation,
        # only on save via Wagtail admin signals.
        call_command("update_index", verbosity=0)

    def test_search_returns_matching_recipe(self):
        results = RecipePage.objects.live().search("cookies")
        titles = [r.title for r in results]
        self.assertIn("Chocolate Chip Cookies", titles)

    def test_search_excludes_nonmatching_recipe(self):
        results = RecipePage.objects.live().search("cookies")
        titles = [r.title for r in results]
        self.assertNotIn("Tomato Soup", titles)

    def test_search_by_ingredient(self):
        # search_fields on RecipePage includes ingredients
        results = RecipePage.objects.live().search("chocolate chips")
        titles = [r.title for r in results]
        self.assertIn("Chocolate Chip Cookies", titles)

    def test_search_view_returns_200_with_results(self):
        factory = RequestFactory()
        request = factory.get("/search/", {"query": "cookies"})
        response = search(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chocolate Chip Cookies")

    def test_search_view_empty_query_returns_200(self):
        factory = RequestFactory()
        request = factory.get("/search/")
        response = search(request)
        self.assertEqual(response.status_code, 200)
