# Generated by Django 5.1.3 on 2024-11-20 04:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_portfolio_options_portfolio_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
