# Generated by Django 3.0.7 on 2020-08-22 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200817_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.IntegerField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(default='SAVINGS', editable=False, max_length=30),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=12),
        ),
    ]