# Generated by Django 4.0.4 on 2022-05-31 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_mrp_id_product_mrp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='mrp',
        ),
    ]
