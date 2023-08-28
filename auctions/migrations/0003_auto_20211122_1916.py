# Generated by Django 3.2.8 on 2021-11-22 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('CL', 'Clothing'), ('JE', 'Jewelry'), ('RE', 'Record'), ('BO', 'Book'), ('AR', 'Art'), ('IN', 'Instrument'), ('KI', 'Kitchen'), ('DE', 'Decoration'), ('OT', 'Other'), (None, 'Choose a category')], default='CL', max_length=2),
        ),
        migrations.AddField(
            model_name='listing',
            name='picture',
            field=models.URLField(blank=True, max_length=350),
        ),
    ]
