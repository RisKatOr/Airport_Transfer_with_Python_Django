# Generated by Django 3.1.7 on 2021-03-29 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210329_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformmessage',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Not Solved', 'Not Solved'), ('Solved', 'Solved')], default='New', max_length=10),
        ),
    ]
