# Generated by Django 5.0.1 on 2024-01-10 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0005_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=12)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
