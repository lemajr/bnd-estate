# Generated by Django 5.1.5 on 2025-01-30 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='image',
        ),
        migrations.AddField(
            model_name='property',
            name='image_public_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
