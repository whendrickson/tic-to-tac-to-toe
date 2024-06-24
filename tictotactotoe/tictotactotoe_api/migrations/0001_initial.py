# Generated by Django 5.0.6 on 2024-06-18 14:01

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='turn_x', max_length=16)),
                ('player_o', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='player_o', to=settings.AUTH_USER_MODEL)),
                ('player_x', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='player_x', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Moves',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('player', models.CharField(choices=[('x', 'x'), ('o', 'o')], max_length=1)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tictotactotoe_api.games')),
            ],
        ),
    ]