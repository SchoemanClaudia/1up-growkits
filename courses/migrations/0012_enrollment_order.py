# Generated by Django 3.2.25 on 2025-04-16 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_alter_order_status'),
        ('courses', '0011_enrollment_spots_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enrollments', to='checkout.order'),
        ),
    ]
