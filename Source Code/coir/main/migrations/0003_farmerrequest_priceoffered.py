# Generated by Django 5.1.3 on 2024-11-21 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_farmerrequest_alter_industryrequirement_industryname'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmerrequest',
            name='priceOffered',
            field=models.IntegerField(default=0),
        ),
    ]
