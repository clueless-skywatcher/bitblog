# Generated by Django 3.1 on 2020-08-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_bloguser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
