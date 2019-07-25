# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-19 08:39
from __future__ import unicode_literals

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
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u5b66\u6821')),
                ('company', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u516c\u53f8')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u5730\u5740')),
                ('profession', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u804c\u4e1a')),
                ('aboutme', models.TextField(blank=True, null=True, verbose_name='\u7b80\u4ecb')),
                ('modify_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65e5\u671f')),
                ('image', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u4e2a\u4eba\u4fe1\u606f',
                'verbose_name_plural': '\u4e2a\u4eba\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth', models.DateField(blank=True, null=True, verbose_name='\u751f\u65e5')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='\u8054\u7cfb\u65b9\u5f0f')),
                ('resgister_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6ce8\u518c\u65e5\u671f')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237\u540d')),
            ],
            options={
                'verbose_name': '\u6ce8\u518c\u4fe1\u606f',
                'verbose_name_plural': '\u6ce8\u518c\u4fe1\u606f',
            },
        ),
    ]
