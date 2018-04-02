# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-02 16:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remetente', models.CharField(blank=True, max_length=30)),
                ('assunto', models.CharField(blank=True, max_length=30)),
                ('mensagem', models.TextField(blank=True, max_length=500)),
                ('dt_mensagem', models.DateTimeField(blank=True, null=True)),
                ('lida', models.BooleanField(default=False)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, max_length=500)),
                ('cidade', models.CharField(blank=True, max_length=30)),
                ('estado', models.CharField(blank=True, max_length=2)),
                ('dt_nascimento', models.DateField(blank=True, null=True)),
                ('foto_perfil', models.FileField(blank=True, null=True, upload_to='perfil/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
