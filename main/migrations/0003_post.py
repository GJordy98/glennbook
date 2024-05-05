# Generated by Django 5.0.3 on 2024-04-30 19:29

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=1000)),
                ('image', models.ImageField(blank=True, upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
    ]
