# Generated by Django 3.2.25 on 2025-03-16 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
