# Generated by Django 3.1.1 on 2020-09-23 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management_app', '0004_auto_20200922_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendencereport',
            name='status',
            field=models.IntegerField(default=False),
        ),
    ]
