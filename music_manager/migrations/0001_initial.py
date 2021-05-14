# Generated by Django 3.2.2 on 2021-05-14 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_name', models.CharField(blank=True, max_length=255, null=True)),
                ('music_url', models.CharField(blank=True, max_length=255, null=True)),
                ('music_artist', models.CharField(blank=True, max_length=255, null=True)),
                ('album', models.CharField(blank=True, max_length=255, null=True)),
                ('album_url', models.CharField(blank=True, max_length=255, null=True)),
                ('music_duration', models.IntegerField(blank=True, null=True)),
                ('played', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('playlist_author', models.CharField(blank=True, max_length=255, null=True)),
                ('playlist_url', models.CharField(max_length=255)),
                ('playlist_uuid', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]