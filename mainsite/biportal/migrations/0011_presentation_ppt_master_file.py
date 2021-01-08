# Generated by Django 3.1.5 on 2021-01-07 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biportal', '0010_bipage_ppt_page_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='ppt_master_file',
            field=models.CharField(blank=True, choices=[('master1', 'Guardian Master PPT')], default='master1', max_length=20, null=True, verbose_name='PPT Master Layout'),
        ),
    ]
