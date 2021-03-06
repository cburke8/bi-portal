# Generated by Django 3.1.5 on 2021-01-07 19:34

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('biportal', '0008_auto_20210107_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='h',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='w',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='x',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='y',
            field=models.FloatField(default=0),
        ),
    ]
