# Generated by Django 2.0.2 on 2018-04-06 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20180406_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyinstance',
            name='borrower',
            field=models.CharField(help_text='Enter the full name of the person who will be responsible for the key', max_length=100),
        ),
    ]
