# Generated by Django 2.2.1 on 2019-06-24 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
        ('authorization', '0004_auto_20190611_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='menu',
            field=models.ManyToManyField(to='apis.App'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['nickname'], name='authorizati_nicknam_b76290_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['open_id'], name='authorizati_open_id_8675f5_idx'),
        ),
    ]
