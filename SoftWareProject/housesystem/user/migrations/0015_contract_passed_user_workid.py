# Generated by Django 4.0.3 on 2022-06-04 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_contract_contractid_alter_order_mark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='Passed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='WorkID',
            field=models.IntegerField(default=0, null=True),
        ),
    ]