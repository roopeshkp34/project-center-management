# Generated by Django 3.1.1 on 2020-09-20 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='attendence_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]