# Generated by Django 3.0.7 on 2020-10-04 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
