# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
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

md_format_help = 'This text will be formatted with markdown.'


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(help_text='This will override the default caption.'+md_format_help,
                               blank=True, null=True, required=False)

    class Meta:
        icon = 'image'
        template = 'blog/captioned_image_block.html'
        label = 'Image'


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    author = blocks.CharBlock()

    class Meta:
        icon = 'openquote'
        template = 'blog/quote.html'


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

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Category"

    # TODO: Write function to list all recipes in category


class CategoryGroupPage(Page):
    """
    Categorization group (e.g., "meat" which has individual categories under it
    Only categories are applied to recipes (not category groups), but recipes will show up under grouping
    """
    parent_page_types = ['CategoryIndexPage']
    subpage_types = [CategoryPage]

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

class Ingredient(Orderable):
    page = ParentalKey('RecipePage', related_name='ingredients')
    quantity = models.CharField(max_length=64)
    unit = models.CharField(max_length=128)
    ingredient = models.CharField(max_length=512)

    panels = [
        FieldRowPanel([
            FieldPanel('quantity', classname='col3'),
            FieldPanel('unit', classname='col3'),
            FieldPanel('ingredient', classname='col6'),
        ], classname="label-above")
    ]


class Instruction(Orderable):
    page = ParentalKey('RecipePage', related_name='instructions')
    instruction = models.TextField(verbose_name='')

    panels = [
        FieldPanel('instruction')
    ]


class RecipePage(Page):
    parent_page_types = ["RecipeIndexPage",]
    subpage_types = []

    # TODO: Add source, nutrition info, servings, cook/prep time

    main_image = models.ForeignKey(
        'images.CustomImage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = models.TextField(
        max_length=250,
        help_text='Appears above the recipe and on preview pages. '+md_format_help)

    prep_time = models.IntegerField(blank=True, null=True, verbose_name='Prep time (min.)')
    cook_time = models.IntegerField(blank=True, null=True, verbose_name='Prep time (min.)')
    servings = models.CharField(max_length=127, blank=True)
    source_name = models.CharField(max_length=255, blank=True, verbose_name='Source')
    source_url = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('main_image'),
        InlinePanel('recipe_categories', label='Categories'),

        FieldPanel('intro'),
        FieldRowPanel([
            FieldPanel('prep_time', classname='col3'),
            FieldPanel('cook_time', classname='col3'),
            FieldPanel('servings', classname='col3'),
        ], classname='label-above'),

        FieldRowPanel([
            FieldPanel('source_name', classname='col6'),
            FieldPanel('source_url', classname='col6')
        ], classname='label-above'),

        InlinePanel('ingredients', label='Ingredients'),
        InlinePanel('instructions', label='Instructions'),
        #StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Recipe"

    def __unicode__(self):
        return self.title

    def subject(self):
        # Find closest ancestor which is recipe index page
        return self.get_ancestors().type(RecipeIndexPage).last()

    """def subject(self):
        # TODO: Replace/remove
        subject = ArticleIndexPage.objects.ancestor_of(self).last().subject
        if subject is not None:
            return subject
        else:
            return ""
    """

    """
    def all_subjects(self):
        # TODO: Replace/remove
        subjects = []
        for s in SubjectPage.objects.all():
            subjects.append(ArticleIndexPage.objects.filter(subject=s)[0])
        return subjects
    """


class RecipeIndexPage(Page):
    """
    Root page under which all recipe pages are made.
    There should only be one of these, at the top level
    """
    subpage_types = ['RecipePage']

    class Meta:
        verbose_name = 'Recipes Index'

    def get_context(self, request, *args, **kwargs):
        context = super(RecipeIndexPage, self).get_context(
            request, *args, **kwargs)
        recipes = self.recipes()

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

    def recipes(self, subject_filter=None):
        """
        Return all recipes if no subject specified, otherwise only those from that Subject
        :param subject_filter: Subject
        :return: QuerySet of Recipes (I think)
        """
        recipes = RecipePage.objects.live().descendant_of(self)
        if subject_filter is not None:
            recipes = recipes.filter(Q(subject_1=subject_filter) | Q(subject_2=subject_filter))
        recipes = recipes.order_by('-date')
        return recipes
