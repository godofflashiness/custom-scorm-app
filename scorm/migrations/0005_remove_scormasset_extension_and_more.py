# Generated by Django 5.0.4 on 2024-04-11 22:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorm', '0004_scormasset_extension_scormasset_filename_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scormasset',
            name='extension',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='full_path_name',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='message',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='reference',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='scormdir',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='size',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='status',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='zipfilename',
        ),
        migrations.RemoveField(
            model_name='scormasset',
            name='zippath',
        ),
        migrations.CreateModel(
            name='ScormResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(null=True)),
                ('message', models.TextField(null=True)),
                ('scormdir', models.TextField(null=True)),
                ('full_path_name', models.TextField(null=True)),
                ('size', models.BigIntegerField(null=True)),
                ('zippath', models.TextField(null=True)),
                ('zipfilename', models.TextField(null=True)),
                ('extension', models.CharField(max_length=10, null=True)),
                ('filename', models.TextField(null=True)),
                ('reference', models.TextField(null=True)),
                ('scorm', models.CharField(max_length=50, null=True)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='scorm.scormasset')),
            ],
        ),
    ]
