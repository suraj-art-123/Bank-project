# Generated by Django 3.0.7 on 2020-08-17 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200817_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='acount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Account'),
        ),
    ]
