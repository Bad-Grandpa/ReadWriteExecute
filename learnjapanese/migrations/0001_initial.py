# Generated by Django 4.0.6 on 2022-10-10 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FlashCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english_text', models.CharField(max_length=100)),
                ('japanese_text', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(verbose_name='date created')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnjapanese.category')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(max_length=100)),
                ('flash_cards', models.ManyToManyField(to='learnjapanese.flashcard')),
            ],
        ),
    ]
