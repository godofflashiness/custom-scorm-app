# Generated by Django 5.0.4 on 2024-04-15 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0012_rename_scrom_consumed_clientuser_scorm_consumed"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="domains",
            field=models.TextField(
                blank=True, help_text="Enter the domains separated by commas", null=True
            ),
        ),
    ]