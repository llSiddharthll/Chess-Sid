# Generated by Django 5.0.1 on 2024-02-15 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chessapp', '0014_userprofile_full_name_userprofile_matches_draw_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='result',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
