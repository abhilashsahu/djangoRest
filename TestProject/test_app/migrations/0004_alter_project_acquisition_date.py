# Generated by Django 4.1.7 on 2023-02-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_alter_project_company_id_delete_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='acquisition_date',
            field=models.DateTimeField(null=True),
        ),
    ]
