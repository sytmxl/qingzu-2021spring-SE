# Generated by Django 3.2.5 on 2022-05-20 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='UserName',
            new_name='Username',
        ),
    ]
