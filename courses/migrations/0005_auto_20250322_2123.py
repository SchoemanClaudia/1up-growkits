# Generated by Django 3.2.25 on 2025-03-22 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_attendee_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='video_url',
        ),
        migrations.AddField(
            model_name='course',
            name='location',
            field=models.CharField(blank=True, help_text='Physical location of the course', max_length=255, null=True),
        ),
    ]
