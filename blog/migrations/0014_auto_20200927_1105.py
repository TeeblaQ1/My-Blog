# Generated by Django 3.0.10 on 2020-09-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200924_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='keywords',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
