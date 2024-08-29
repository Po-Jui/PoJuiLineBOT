# Generated by Django 3.2.9 on 2021-11-24 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='', max_length=50)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('pic_url', models.CharField(max_length=255)),
                ('mtext', models.CharField(blank=True, max_length=255)),
                ('mdt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
