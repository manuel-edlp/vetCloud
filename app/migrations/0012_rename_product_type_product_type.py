# Generated by Django 5.0.4 on 2024-06-12 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_type',
            new_name='type',
        ),
    ]