# Generated by Django 4.0.4 on 2022-04-28 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_toy_alter_feeding_options_alter_feeding_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toy',
            name='color',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='toy',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]
