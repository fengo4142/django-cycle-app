# Generated by Django 2.1.7 on 2019-08-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycle', '0018_auto_20190725_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle_in_obj',
            name='year',
            field=models.IntegerField(choices=[(2019, 2019), (2020, 2020)], default=2019),
            preserve_default=False,
        ),
    ]
