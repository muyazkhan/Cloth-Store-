# Generated by Django 5.0 on 2024-01-23 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_alter_review_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AverageRating',
        ),
    ]
