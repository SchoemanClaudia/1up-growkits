# Generated by Django 3.2.25 on 2025-04-16 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_enrollment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(blank=True, help_text='The date the course starts', null=True),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Enrolled', 'Enrolled'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
