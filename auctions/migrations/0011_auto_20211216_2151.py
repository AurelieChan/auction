# Generated by Django 3.2.8 on 2021-12-16 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20211216_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentedby', to='auctions.user'),
            preserve_default=False,
        ),
    ]