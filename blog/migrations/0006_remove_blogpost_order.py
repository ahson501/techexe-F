# Generated by Django 5.1.2 on 2024-10-30 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_blogpost_course_delete_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='order',
        ),
    ]
