# Generated by Django 5.1.5 on 2025-01-28 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iccbs', '0008_profile_availability_profile_certifications_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
