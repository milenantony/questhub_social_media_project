# Generated by Django 5.0.3 on 2024-03-17 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questhub_app', '0006_registerprofile_profile_picture_alter_questions_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
