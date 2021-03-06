# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-28 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_auto_20180327_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='davp_constraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=40, max_digits=1000)),
                ('longitude', models.DecimalField(decimal_places=40, max_digits=1000)),
                ('s_date', models.IntegerField()),
                ('s_month', models.IntegerField()),
                ('s_year', models.IntegerField()),
                ('e_date', models.IntegerField()),
                ('e_month', models.IntegerField()),
                ('e_year', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='image',
            old_name='encrypted_code',
            new_name='generated_hash',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='hash_code',
            new_name='hashcode',
        ),
        migrations.RemoveField(
            model_name='image',
            name='hours',
        ),
        migrations.RemoveField(
            model_name='image',
            name='id',
        ),
        migrations.RemoveField(
            model_name='image',
            name='minutes',
        ),
        migrations.RemoveField(
            model_name='image',
            name='picture',
        ),
        migrations.AddField(
            model_name='image',
            name='Uid',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='location',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='pic',
            field=models.ImageField(default=0, upload_to=b''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='date',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='image',
            name='latitude',
            field=models.DecimalField(decimal_places=40, max_digits=1000),
        ),
        migrations.AlterField(
            model_name='image',
            name='longitude',
            field=models.DecimalField(decimal_places=40, max_digits=1000),
        ),
        migrations.AlterField(
            model_name='image',
            name='month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='image',
            name='year',
            field=models.IntegerField(),
        ),
    ]
