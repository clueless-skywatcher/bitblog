# Generated by Django 3.1.5 on 2021-01-24 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_auto_20210117_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilecard',
            name='img_small',
        ),
    ]
