# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                FieldRowPanel,
                                                InlinePanel,
                                                PageChooserPanel,
                                                StreamFieldPanel)
from utils import format_ingredient_line

md_format_help = 'This text will be formatted with markdown.'


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(help_text='This will override the default caption.'+md_format_help,
                               blank=True, null=True, required=False)

    class Meta:
        icon = 'image'
        template = 'blog/captioned_image_block.html'
        label = 'Image'


class CategoryPage(Page):
    """
    Identifies the different categories to apply to recipes (can apply multiple to a recipe)
    """
    parent_page_types = ['CategoryIndexPage', 'CategoryGroupPage']
    subpage_types = []

    description = models.TextField(
        max_length=800,
        null=True, blank=True,
        help_text=md_format_help)

    icon = models.ForeignKey(
        'images.CustomImage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This should be a square line-based icon in the right color'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('icon'),
        FieldPanel('description'),
    ]

    def __unicode__(self):
        parent_page = self.get_parent()
        if parent_page.specific_class == CategoryGroupPage:
            return str(parent_page) + ': ' + self.title
        else:
            return self.title

    class Meta:
        verbose_name = "Category"

    def get_context(self, request, *args, **kwargs):
        """
        Add recipes to the context for recipe category listings
        """
        context = super(CategoryPage, self).get_context(
            request, *args, **kwargs)
        recipes = self.get_recipes()

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        from home.models import GeneralSettings
        if GeneralSettings.for_site(request.site).pagination_count:
            page_size = GeneralSettings.for_site(request.site).pagination_count

        if page_size is not None:
            paginator = Paginator(recipes, page_size)
            try:
                recipes = paginator.page(page)
            except PageNotAnInteger:
                recipes = paginator.page(1)
            except EmptyPage:
                recipes = paginator.page(paginator.num_pages)

        context['recipes'] = recipes
        return context

    def get_recipes(self):
        """
        Return all recipes if no subject specified, otherwise only those from that Subject
        :param subject_filter: Subject
        :return: QuerySet of Recipes (I think)
        """
        recipes = RecipePage.objects.live()
        recipes = recipes.filter(recipe_categories__category=self)
        recipes = recipes.order_by('-post_date')
        return recipes


class CategoryGroupPage(Page):
    """
    Categorization group (e.g., "meat" which has individual categories under it
    Only categories are applied to recipes (not category groups), but recipes will show up under grouping
    """
    parent_page_types = ['CategoryIndexPage']
    subpage_types = [CategoryPage]

    icon = models.ForeignKey(
        'images.CustomImage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This should be a square line-based icon in the right color'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('icon'),
    ]

    class Meta:
        verbose_name = "Category Group"

    # TODO: Write function to list all categories
    # TODO: Write funciton to list all recipes in category group


class CategoryIndexPage(Page):
    """
    Top-level page (should only be one) under which to categorize recipes
    """

    subpage_types = [CategoryPage, CategoryGroupPage]

    class Meta:
        verbose_name = "Recipe Categories Index"

    def list_categories(self):
        """
        List ALL categories
        :return:
        """
        return CategoryPage.objects.all()
        # TODO: Category listing ignores hierarchy


class CategoryLink(Orderable):
    page = ParentalKey('RecipePage', related_name='recipe_categories')
    category = models.ForeignKey(CategoryPage)

    panels = [
        PageChooserPanel('category')
    ]


class RecipePage(Page):
    parent_page_types = ["RecipeIndexPage",]
    subpage_types = []

    # TODO: nutrition info

    post_date = models.DateField(null=True)

    main_image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Image should be at least 1280x512 px'
    )
    intro = models.TextField(
        max_length=250,
        help_text='Appears above the recipe and on preview pages. '+md_format_help)

    prep_time = models.DurationField(blank=True, null=True)
    cook_time = models.DurationField(blank=True, null=True)
    total_time = models.DurationField(blank=True, null=True)
    recipe_yield = models.CharField(max_length=127, blank=True, verbose_name='Yield')
    source_name = models.CharField(max_length=255, blank=True, verbose_name='Source')
    source_url = models.URLField(blank=True)

    ingredients = models.TextField(blank=True, help_text='One ingredient per line. Make separate sections with a square bracketed line like [section name]. '+md_format_help)
    instructions = models.TextField(blank=True, help_text='Each new line generates a new numbered instruction. '+md_format_help)

    notes = models.TextField(blank=True, help_text='Additional notes such as substitutions. '+md_format_help)

    content_panels = Page.content_panels + [
        FieldPanel('post_date'),
        ImageChooserPanel('main_image'),
        InlinePanel('recipe_categories', label='Categories'),

        FieldPanel('intro'),
        FieldRowPanel([
            FieldPanel('prep_time', classname='col3'),
            FieldPanel('cook_time', classname='col3'),
            FieldPanel('total_time', classname='col3'),
            FieldPanel('recipe_yield', classname='col3'),
        ], classname='label-above'),

        FieldRowPanel([
            FieldPanel('source_name', classname='col6'),
            FieldPanel('source_url', classname='col6')
        ], classname='label-above'),

        FieldPanel('ingredients'),
        FieldPanel('notes'),
        FieldPanel('instructions'),
        #InlinePanel('instructions', label='Instructions'),
    ]

    def format_ingredients(self):
        """
        Format the ingredients field into Markdown, which can be formatted with make_markdown in the template
        :return: String of Markdown-formatted ingredients
        """
        lines = [format_ingredient_line(line) for line in self.ingredients.splitlines()]
        return '\n'.join(lines)

    def format_instructions(self):
        """
        Format the instructions string into a Markdown ordered list, which can be formatted with make_markdown in the template
        :return:  String of Markdown-formatted instructions (ordered list)
        """
        lines = self.instructions.splitlines()
        for ind, line in enumerate(lines):
            if len(line) > 0 and not line.isspace():
                lines[ind] = '{}. {}'.format(ind, line)
        return '\n'.join(lines)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('ingredients'),
        index.SearchField('instructions')
    ]

    class Meta:
        verbose_name = "Recipe"

    def __unicode__(self):
        return self.title


class RecipeIndexPage(Page):
    """
    Root page under which all recipe pages are made.
    There should only be one of these, at the top level
    """
    subpage_types = ['RecipePage']

    class Meta:
        verbose_name = 'Recipes Index'

    def get_context(self, request, *args, **kwargs):
        """
        Add recipes to the context for recipe category listings
        """
        context = super(RecipeIndexPage, self).get_context(
            request, *args, **kwargs)
        recipes = self.get_recipes()

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        from home.models import GeneralSettings
        if GeneralSettings.for_site(request.site).pagination_count:
            page_size = GeneralSettings.for_site(request.site).pagination_count

        if page_size is not None:
            paginator = Paginator(recipes, page_size)
            try:
                recipes = paginator.page(page)
            except PageNotAnInteger:
                recipes = paginator.page(1)
            except EmptyPage:
                recipes = paginator.page(paginator.num_pages)

        context['recipes'] = recipes
        return context

    def get_recipes(self):
        """
        Return all recipes if no subject specified, otherwise only those from that Subject
        :param subject_filter: Subject
        :return: QuerySet of Recipes (I think)
        """
        recipes = RecipePage.objects.live()
        recipes = recipes.order_by('-post_date')
        return recipes
