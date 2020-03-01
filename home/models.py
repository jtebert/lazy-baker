from __future__ import absolute_import, unicode_literals

from modelcluster.fields import ParentalKey

from django.db import models

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from recipes.models import RecipePage, CaptionedImageBlock, CategoryPage

md_format_help = 'This text will be formatted with markdown.'
DEFAULT_RICHTEXT_FEATURES = [
    'h2', 'h3', 'h4', 'h5',
    'bold', 'italic', 'strikethrough', 'code',
    'ol', 'ul',
    'hr',
    'link',
    'document-link',
]


class HomePage(Page):
    """
    Home landing page for the entire site.

    This shows a featured recipe and a list of the most recently posted recipes.
    """
    parent_page_types = ['wagtailcore.Page']

    body = models.TextField(blank=True, help_text=md_format_help)
    logo = models.ForeignKey(
        'images.CustomImage',
        null=True,
        on_delete=models.SET_NULL
    )
    num_recent_recipes = models.PositiveIntegerField(default=6)
    featured_recipe = models.ForeignKey(
        RecipePage,
        null=True, blank=True,
        on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        ImageChooserPanel('logo'),
        PageChooserPanel('featured_recipe'),
    ]

    class Meta:
        verbose_name = "Homepage"

    def get_context(self, request, *args, **kwargs):
        """
        Add recipes to the context for recipe category listings
        """
        context = super(HomePage, self).get_context(
            request, *args, **kwargs)
        recent_recipes = RecipePage.objects.live().order_by('-post_date')[:self.num_recent_recipes]

        context['recent_recipes'] = recent_recipes
        return context


class AboutPage(Page):
    """
    An accessory page that can be added to show general information about the site.
    """

    parent_page_types = ['HomePage']
    subpage_types = []

    body = StreamField([
        ('text', blocks.RichTextBlock(features=DEFAULT_RICHTEXT_FEATURES)),
        ('captioned_image', CaptionedImageBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


@register_setting
class GeneralSettings(BaseSetting):
    site_name = models.CharField(
        max_length=127,
        help_text='Website name')
    site_author = models.CharField(
        max_length=127,
        blank=True,
        help_text='Claim credit')
    site_icon = models.ForeignKey(
        'images.CustomImage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This should be a square line-based icon in the right color'
    )
    site_tagline = models.CharField(
        max_length=255,
        blank=True,
        help_text='Tagline to show after the site title'
    )
    site_description = models.TextField(
        blank=True,
        help_text='Description of website (to appear on searches)',
    )
    contact_email = models.EmailField(
        blank=True,
        help_text='Publically displayed contact information'
    )
    recipe_icon = models.ForeignKey(
        'images.CustomImage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This should be a square line-based icon in the right color'
    )
    pagination_count = models.PositiveIntegerField(
        default=10,
        help_text="Number of posts to display per page on index pages")
    disqus = models.CharField(
        max_length=127,
        null=True, blank=True,
        help_text="Site name on Disqus. Comments will only appear if this is provided.")
    google_analytics_id = models.CharField(
        max_length=127,
        blank=True, null=True,
        help_text='Google Analytics Tracking ID')
    random_recipe_category = models.ForeignKey(
        CategoryPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Which Category will random recipes be selected from')
    random_recipe_icon = models.ForeignKey(
        'images.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This should be a square line-based icon in the right color'
    )

    panels = [
        FieldPanel('site_name'),
        FieldPanel('site_author'),
        ImageChooserPanel('site_icon'),
        FieldPanel('site_tagline'),
        FieldPanel('site_description'),
        FieldPanel('contact_email'),
        ImageChooserPanel('recipe_icon'),
        FieldPanel('pagination_count'),
        FieldPanel('disqus'),
        FieldPanel('google_analytics_id'),
        PageChooserPanel('random_recipe_category'),
        ImageChooserPanel('random_recipe_icon'),
    ]


@register_setting(icon='group')
class SocialMediaSettings(BaseSetting):
    twitter_username = models.CharField(max_length=127, blank=True)
    github_username = models.CharField(max_length=127, blank=True)
    #facebook_url = models.CharField(max_length=127, blank=True, help_text='This is the part after the / on the address of your profile')
    #snapchat_username = models.CharField(max_length=127, blank=True)
    instagram_username = models.CharField(max_length=127, blank=True)
    #medium_username = models.CharField(max_length=127, blank=True)
    linkedin_url = models.CharField(max_length=127, blank=True,
                                    help_text='This is the part after the /in/ on the address of your profile')

    panels = [
        FieldPanel('github_username'),
        FieldPanel('instagram_username'),
        FieldPanel('linkedin_url'),
        FieldPanel('twitter_username'),
    ]

    class Meta:
        verbose_name = 'Social media accounts'
