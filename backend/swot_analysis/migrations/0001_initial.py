# Generated by Django 3.1.5 on 2021-01-22 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SWOTAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Analysis title')),
                ('description', models.CharField(max_length=300, null=True, verbose_name='Analysis short description')),
                ('starting_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('state', models.IntegerField(choices=[(1, 'In progress'), (2, 'Closed'), (3, 'Archived')], default=1)),
            ],
        ),
    ]