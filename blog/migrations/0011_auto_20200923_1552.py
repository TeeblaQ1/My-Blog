# Generated by Django 3.0.10 on 2020-09-23 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200923_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, default='pictures/blog-post-thumb-1.jpg', null=True, upload_to='thumbnail/%Y/%m/%d'),
        ),
    ]
