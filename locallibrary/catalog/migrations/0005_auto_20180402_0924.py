# Generated by Django 2.0.2 on 2018-04-02 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180328_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='urgency',
            field=models.CharField(choices=[('2', 'Low'), ('1', 'Medium'), ('0', 'High')], default='2', max_length=1),
        ),
    ]
