# Generated by Django 4.2.4 on 2023-08-10 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direct', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='directmessage',
            name='message',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]