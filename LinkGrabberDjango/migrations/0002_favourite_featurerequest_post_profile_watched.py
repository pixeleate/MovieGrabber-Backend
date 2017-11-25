# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-16 16:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LinkGrabberDjango', '0001_initial'),
    ]

    operations = [

        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('rating', models.FloatField(max_length=10)),
                ('poster', models.URLField()),
                ('year', models.IntegerField(max_length=10)),
            ],
        )
    ]