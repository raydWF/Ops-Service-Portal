# Generated by Django 2.0.2 on 2018-03-27 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20180326_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='request_comments',
            field=models.TextField(help_text='Enter a brief description of the request', max_length=100),
        ),
    ]
