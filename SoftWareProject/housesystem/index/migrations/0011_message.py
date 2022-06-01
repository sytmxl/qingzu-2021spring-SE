from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_alter_house_area_alter_house_floor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('MessageID', models.IntegerField(primary_key=True, serialize=False)),
                ('WorkID', models.IntegerField(null=True)),
                ('Errornumber', models.IntegerField(null=True)),
                ('UserID', models.IntegerField()),
                ('Text', models.TextField(null=True)),
                ('Username', models.CharField(max_length=255)),
            ],
        ),
    ]
