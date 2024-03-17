# Generated by Django 5.0.3 on 2024-03-17 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questhub_app', '0005_alter_questions_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='dp.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='questions',
            name='time',
            field=models.TimeField(auto_now=True, null=True),
        ),
    ]
