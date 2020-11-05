# Generated by Django 3.1.2 on 2020-11-05 00:26

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('img', models.ImageField(upload_to='profile_cards')),
                ('img_small', models.ImageField(upload_to='profile_cards_small')),
            ],
        ),
        migrations.CreateModel(
            name='Sigil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('img', models.ImageField(upload_to='sigils')),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(default='No description', max_length=250)),
                ('hometown', models.CharField(default='Not specified', max_length=200)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('current_profile_card', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.profilecard')),
                ('current_sigil', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.sigil')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', ckeditor.fields.RichTextField()),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('votes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('comment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('votes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost')),
            ],
        ),
        migrations.CreateModel(
            name='SigilGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigil', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.sigil')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sigils', to='blog.bloguser')),
            ],
            options={
                'unique_together': {('user', 'sigil')},
            },
        ),
        migrations.CreateModel(
            name='ProfileCardGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.profilecard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_cards', to='blog.bloguser')),
            ],
            options={
                'unique_together': {('user', 'profile_card')},
            },
        ),
    ]
