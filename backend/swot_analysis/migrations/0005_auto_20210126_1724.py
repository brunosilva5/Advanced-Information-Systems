# Generated by Django 3.1.5 on 2021-01-26 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swot_analysis', '0004_auto_20210126_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swotanalysis',
            name='state',
            field=models.IntegerField(choices=[(1, 'Open'), (2, 'Closed')], default=1),
        ),
    ]