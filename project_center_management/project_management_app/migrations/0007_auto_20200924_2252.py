# Generated by Django 3.1.1 on 2020-09-24 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management_app', '0006_auto_20200923_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='attendence_date',
            field=models.DateField(),
        ),
    ]
