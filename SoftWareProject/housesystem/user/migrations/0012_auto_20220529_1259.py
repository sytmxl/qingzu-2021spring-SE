# Generated by Django 3.2.5 on 2022-05-29 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20220528_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='DueDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='OrderDate',
            field=models.DateField(),
        ),
    ]
