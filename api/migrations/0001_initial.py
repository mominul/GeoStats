# Generated by Django 4.2.7 on 2023-11-03 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_id', models.IntegerField()),
                ('country', models.TextField(max_length=255)),
                ('city', models.TextField(max_length=255, null=True)),
                ('name', models.TextField(max_length=255, null=True)),
                ('code', models.CharField(max_length=255)),
            ],
        ),
    ]
