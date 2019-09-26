# Generated by Django 2.2.5 on 2019-09-26 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluidol_index', '0006_auto_20181213_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product_applications',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product_benefits',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product_features',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
