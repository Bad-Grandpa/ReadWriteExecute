# Generated by Django 4.0.8 on 2022-12-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnjapanese', '0002_alter_flashcard_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='japanese_text_kanji',
            field=models.CharField(max_length=100, null=True),
        ),
    ]