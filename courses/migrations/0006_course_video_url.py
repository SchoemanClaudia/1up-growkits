# Generated by Django 3.2.25 on 2025-03-22 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20250322_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video_url',
            field=models.URLField(blank=True, help_text='Private video link for enrolled users', null=True),
        ),
    ]
