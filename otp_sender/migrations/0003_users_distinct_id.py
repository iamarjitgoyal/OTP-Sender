# Generated by Django 4.2.1 on 2023-06-01 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_sender', '0002_users_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='distinct_id',
            field=models.CharField(default='arjit_goyal', max_length=50),
        ),
    ]
