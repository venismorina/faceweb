# Generated by Django 2.2.13 on 2020-07-04 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendreq', '0007_auto_20200704_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detection',
            name='date',
            field=models.DateTimeField(default=None),
        ),
    ]
