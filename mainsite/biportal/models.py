import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator
from taggit.managers import TaggableManager
from django.utils import timezone
from django.utils.html import format_html

from PIL import Image
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import ImageField
from markdown import markdown

# references:
# for sorl.thumbnail: https://sorl-thumbnail.readthedocs.io/en/latest/examples.html

ppt_master_choices = [
    ('master1', 'Guardian Master PPT'),
]

###########################################################################################################
class Presentation(models.Model):

    name = models.CharField(
        max_length=200,
        # unique=True
        )

    description = models.CharField(
        max_length=1000,
        default='',
        blank=True
        )

    ppt_file = models.FileField(
        upload_to='exported_pres_ppt/',
        null = True,
        blank = True,
        verbose_name = 'Exported PPT file',
        )

    pdf_file = models.FileField(
        upload_to='exported_pres_pdf/',
        null = True,
        blank = True,
        verbose_name = 'Exported PDF file'
        )

    ppt_master_file = models.CharField(
        max_length = 20,
        null = True,
        blank = True,
        choices = ppt_master_choices,
        default = 'master1',
        verbose_name = 'PPT Master Layout'
        )

    created_by = models.ForeignKey(
        User,
        related_name='creator',
        null = True,
        on_delete=models.CASCADE
        )

    updated_by = models.ForeignKey(
        User,
        related_name='updater',
        null = True,
        on_delete=models.CASCADE
        )

    created_at = models.DateTimeField(
        editable=False,
        auto_now=True,
        # default=timezone.now()
        )

    updated_at = models.DateTimeField(
        auto_now_add=True,
        # default=timezone.now()
        )

    active = models.BooleanField(
        default=True
        )

    tags = TaggableManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Presentation'
        verbose_name_plural = 'Presentations'
        ordering = ["-created_at"]

###########################################################################################################
class SnippetHtml(models.Model):
    name = models.CharField(
        max_length=200,
        null = True,
        blank = True,
        verbose_name = 'Title'
        )

    htmltext = models.TextField(
        null = True,
        blank = True,
        verbose_name= 'Content'
        )

    def get_htmltext_as_markdown(self):
        return mark_safe(markdown(self.htmltext, safe_mode='escape'))

        # return mark_safe(self.htmltext)
        # return htmltext

    get_htmltext_as_markdown.short_description = 'Content preview'


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'HTML Text'
        verbose_name_plural = 'HTML Texts'

###########################################################################################################
class Snippet(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True
        )

    # embedded = models.TextField(
    embedded = models.CharField(
        max_length=2000,
        blank=True
        )

    # file will be uploaded to MEDIA_ROOT/image_rendered
    image_rendered = models.ImageField(
        upload_to='image_rendered/',
        verbose_name='Rendered Report',
        null = True,
        blank = True
        )

    # using sorl.thumbnail.ImageField
    image_cropped = ImageField(
        upload_to='image_cropped/',
        verbose_name='Report Snippet',
        null = True,
        blank = True
        )

    # @property
    def render_button(self):
        html = """
        <input type="submit" value="Render report" name="_render_report" id=button_render_report>
        <input type="submit" value="Test button" name="_render_report_test" id=button_render_report_test onClick='alert();return 0;'>"""
        return mark_safe(html)

    render_button.short_description = ''

    x = models.FloatField(
        default=0
        )

    y = models.FloatField(
        default=0
        )

    w = models.FloatField(
        default=0
        )

    h = models.FloatField(
        default=0
        )

    created_at = models.DateTimeField(
        editable=False,
        auto_now=True,
        )

    updated_at = models.DateTimeField(
        auto_now_add=True,
        )

    created_by = models.ForeignKey(
        User,
        related_name='snippet_creator',
        null = True,
        on_delete=models.CASCADE
        )

    updated_by = models.ForeignKey(
        User,
        related_name='snippet_updater',
        null = True,
        on_delete=models.CASCADE
        )

    # will be available as bipage.pages_set and snippet.bipages
    # pages = models.ManyToManyField(Bipage)

    tags = TaggableManager(
        blank = True
        )

    def __str__(self):
        return self.name

    # overwritting save
    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            # img = Image.open(self.image_cropped.path)
            # output_size = (125, 125)
            # img.thumbnail(output_size)
            # img.save(self.image.path)


    class Meta:
        verbose_name = 'snippet'
        verbose_name_plural = 'snippets'

###########################################################################################################
ppt_page_layout_choices = [
    ('header', 'Header Page'),
    ('content1', 'Content With 1 Placeholder'),
    ('content2', 'Content With 2 Columns'),
]
class Bipage(models.Model):

    name = models.CharField(
        max_length=100,
        null = True,
        blank = True,
        verbose_name = 'Internal name'
        )

    title = models.CharField(
        max_length=200,
        null = True,
        blank = True,
        verbose_name = 'Title'
        )

    subtitle = models.CharField(
        max_length=200,
        null = True,
        blank = True,
        verbose_name = 'Subtitle'
        )

    snippets = models.ManyToManyField(
        Snippet,
        # null = True,
        blank = True,
        )

    texts = models.ManyToManyField(
        SnippetHtml,
        # null = True,
        blank = True,

        )

    ppt_file = models.FileField(
        upload_to='exported_pages_ppt/',
        null = True,
        blank = True,
        verbose_name = 'Exported PPT file'
        )

    pdf_file = models.FileField(
        upload_to='exported_pages_pdf/',
        null = True,
        blank = True,
        verbose_name = 'Exported PDF file',
        )

    ppt_page_layout = models.CharField(
        max_length = 200,
        null = True,
        blank = True,
        choices = ppt_page_layout_choices,
        default = 'content1',
        verbose_name = 'PPT Page Layout'
        )

    presentation = models.ForeignKey(
        Presentation,
        related_name='presentations',
        on_delete=models.CASCADE
        )

    last_updated = models.DateTimeField(
        auto_now_add=True
        )


    def page_preview(self):
        html = """
        <iframe src="/bip/{}/page/" scrolling="no"
        style="width:1100px; height:620px; border: 1px solid grey;"></iframe>
        """.format(self.pk)

        return mark_safe(html)

    page_preview.short_description = ''

    def layout_preview(self):

        html = """
        <img src='/static/biportal/img/page_layouts/{}.png' />
        """.format(self.ppt_page_layout)

        return mark_safe(html)

    layout_preview.short_description = ''


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'BI Page'
        verbose_name_plural = 'BI Pages'

