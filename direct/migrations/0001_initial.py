# Generated by Django 4.2.4 on 2023-08-10 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0002_commentlike_like'),
        ('account', '0002_alter_account_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='media/')),
                ('is_read', models.BooleanField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.following')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.follower')),
            ],
        ),
    ]