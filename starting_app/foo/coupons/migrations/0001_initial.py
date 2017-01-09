# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-09 03:17
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
            name='ClaimedCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redeemed', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=64)),
                ('code_l', models.CharField(blank=True, max_length=64, unique=True)),
                ('type', models.CharField(choices=[('percent', 'percent'), ('value', 'value')], max_length=16)),
                ('expires', models.DateTimeField(blank=True, null=True)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('bound', models.BooleanField(default=False)),
                ('bind', models.CharField(choices=[('user', 'user'), ('email', 'email')], default='user', max_length=16)),
                ('email', models.EmailField(blank=True, max_length=256, null=True)),
                ('repeat', models.IntegerField(default=-1)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='claimedcoupon',
            name='coupon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coupons.Coupon'),
        ),
        migrations.AddField(
            model_name='claimedcoupon',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
