# Generated by Django 4.2.4 on 2023-09-18 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_remove_post_archive_remove_post_send_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='location',
        ),
    ]
