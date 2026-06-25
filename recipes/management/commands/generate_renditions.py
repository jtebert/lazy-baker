from django.core.management.base import BaseCommand

from home.models import GeneralSettings, HomePage
from recipes.models import CategoryPage, RecipePage


RECIPE_SPECS = ["fill-416x256", "fill-1920x768", "fill-1104x768"]
CATEGORY_ICON_SPECS = ["fill-128x128", "height-256"]
MENU_ICON_SPECS = ["fill-128x128"]


class Command(BaseCommand):
    help = "Pre-generate image renditions used across the site"

    def _generate(self, image, specs, label):
        for spec in specs:
            try:
                image.get_rendition(spec)
                self.stdout.write(f"  {label} [{spec}]")
            except Exception as e:
                self.stderr.write(f"  ERROR {label} [{spec}]: {e}")

    def handle(self, *args, **options):
        self.stdout.write("Generating recipe image renditions...")
        for recipe in RecipePage.objects.all().select_related("main_image"):
            if recipe.main_image:
                self._generate(recipe.main_image, RECIPE_SPECS, recipe.title)

        self.stdout.write("Generating category icon renditions...")
        for cat in CategoryPage.objects.all().select_related("icon"):
            if cat.icon:
                self._generate(cat.icon, CATEGORY_ICON_SPECS, cat.title)

        self.stdout.write("Generating site menu icon renditions...")
        for settings in GeneralSettings.objects.all():
            for field in ("site_icon", "recipe_icon", "random_recipe_icon"):
                image = getattr(settings, field)
                if image:
                    self._generate(image, MENU_ICON_SPECS, f"GeneralSettings.{field}")

        self.stdout.write("Generating homepage logo renditions...")
        for page in HomePage.objects.all().select_related("logo"):
            if page.logo:
                self._generate(page.logo, ["width-1920"], page.title)

        self.stdout.write(self.style.SUCCESS("Done."))
