# Generated by Django 3.0.8 on 2020-08-25 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_orders_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('items_json', models.CharField(max_length=5000)),
                ('update_desc', models.CharField(max_length=5000)),
            ],
        ),
    ]
