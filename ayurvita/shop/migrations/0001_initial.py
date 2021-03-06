# Generated by Django 4.0.1 on 2022-02-12 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopWelcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('welcome_image1', models.ImageField(upload_to='welcome')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('product_desc', models.CharField(max_length=250)),
                ('brand', models.CharField(max_length=50)),
                ('product_price', models.FloatField()),
                ('product_image1', models.ImageField(upload_to='products')),
                ('product_image2', models.ImageField(upload_to='products')),
                ('product_image3', models.ImageField(blank=True, null=True, upload_to='products')),
                ('quantity', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
