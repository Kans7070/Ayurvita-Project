# Generated by Django 4.0.1 on 2022-03-02 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='mrp_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
