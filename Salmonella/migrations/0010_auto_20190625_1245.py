# Generated by Django 2.1.1 on 2019-06-25 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salmonella', '0009_auto_20190619_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allele',
            name='file_location',
            field=models.FileField(max_length=500, upload_to='./srv/scratch/lanlab/mgtdb/Alleles/'),
        ),
        migrations.AlterField(
            model_name='chromosome',
            name='file_location',
            field=models.FileField(upload_to='./srv/scratch/lanlab/mgtdb/References/'),
        ),
    ]
