# Generated by Django 3.0.7 on 2020-09-14 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_job_applicants'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='job_applicants',
            new_name='job_applicant',
        ),
    ]