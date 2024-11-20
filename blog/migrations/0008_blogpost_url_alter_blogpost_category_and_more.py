# Generated by Django 5.1.3 on 2024-11-18 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_category_blogpost_status_blogpost_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Python', 'Python'), ('Django', 'Django'), ('React', 'React'), ('SNMP', 'SNMP')], max_length=100, unique=True),
        ),
    ]
