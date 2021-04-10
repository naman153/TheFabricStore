# Generated by Django 3.1.3 on 2021-01-07 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210101_0410'),
    ]

    operations = [
        migrations.CreateModel(
            name='enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.IntegerField(max_length=10)),
                ('email', models.CharField(max_length=100, null=True)),
                ('message', models.CharField(max_length=250)),
            ],
        ),
    ]
