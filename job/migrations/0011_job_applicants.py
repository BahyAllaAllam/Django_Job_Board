# Generated by Django 3.0.7 on 2020-09-14 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_job_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='job_applicants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=200)),
                ('portfolio_link', models.URLField()),
                ('cv', models.FileField(upload_to='applicants/')),
                ('cover_letter', models.TextField(max_length=500)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_job', to='job.Job')),
            ],
        ),
    ]
