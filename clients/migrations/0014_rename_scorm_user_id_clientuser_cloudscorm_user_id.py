# Generated by Django 5.0.4 on 2024-04-17 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0013_client_domains"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clientuser",
            old_name="scorm_user_id",
            new_name="cloudscorm_user_id",
        ),
    ]