# Generated by Django 3.0.7 on 2020-08-10 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount_number',
            field=models.IntegerField(default=0),
        ),
    ]
