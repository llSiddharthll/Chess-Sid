# Generated by Django 5.0.1 on 2024-02-09 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chessapp', '0006_game_move_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.CharField(default='w', max_length=1),
        ),
    ]
