# Generated by Django 2.1.1 on 2019-06-18 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salmonella', '0006_auto_20190618_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='cc1_2',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_2')),
            ],
        ),
        migrations.CreateModel(
            name='cc1_3',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_3')),
            ],
        ),
        migrations.CreateModel(
            name='cc1_4',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_4')),
            ],
        ),
        migrations.CreateModel(
            name='cc1_5',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_5')),
            ],
        ),
        migrations.CreateModel(
            name='cc1_6',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_6')),
            ],
        ),
        migrations.CreateModel(
            name='cc1_7',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_7')),
            ],
        ),
        migrations.CreateModel(
            name='cc1_8',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_8')),
            ],
        ),
        migrations.CreateModel(
            name='cc1_9',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc1_9')),
            ],
        ),
        migrations.CreateModel(
            name='cc2_2',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc2_2')),
            ],
        ),
        migrations.CreateModel(
            name='cc2_3',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc2_3')),
            ],
        ),
        migrations.CreateModel(
            name='cc2_4',
            fields=[
                ('identifier', models.IntegerField(primary_key=True, serialize=False)),
                ('merge_timestamp', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('merge_id', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to='Salmonella.cc2_4')),
            ],
        ),
    ]
