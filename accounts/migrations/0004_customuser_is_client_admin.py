# Generated by Django 5.0.4 on 2024-04-13 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_customuser_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_client_admin',
            field=models.BooleanField(default=False),
        ),
    ]
