# Generated by Django 2.0.2 on 2018-04-06 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20180406_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyinstance',
            name='roomkey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.RoomKey', verbose_name='Key'),
        ),
        migrations.AlterField(
            model_name='roomkey',
            name='room_des',
            field=models.CharField(blank=True, help_text='Give a brief description of the key', max_length=200, null=True, verbose_name='Key description'),
        ),
        migrations.AlterField(
            model_name='roomkey',
            name='room_name',
            field=models.CharField(blank=True, help_text='Enter the name of the key.', max_length=100, null=True, verbose_name='Key name'),
        ),
    ]
