# Generated by Django 3.0.7 on 2020-11-10 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0016_remove_job_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
