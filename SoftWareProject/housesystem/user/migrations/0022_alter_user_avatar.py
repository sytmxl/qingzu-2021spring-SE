# Generated by Django 3.2.5 on 2022-06-07 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_rename_file_url_contract_filepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(default='', null=True, upload_to=''),
        ),
    ]
