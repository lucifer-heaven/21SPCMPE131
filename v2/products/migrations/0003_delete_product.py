# Generated by Django 3.1.7 on 2021-04-15 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_summary'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
