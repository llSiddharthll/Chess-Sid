# Generated by Django 5.0.1 on 2024-02-14 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chessapp', '0011_userprofile_other_side'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='fen',
            field=models.CharField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', max_length=225),
        ),
    ]
