# Generated by Django 3.1.3 on 2021-01-09 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_feedback_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='slug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
    ]