# Generated by Django 4.2.4 on 2023-08-31 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
