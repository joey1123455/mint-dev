# Generated by Django 5.0.1 on 2024-01-19 16:12

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
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('pin', models.CharField(max_length=4)),
                ('limit_level', models.PositiveIntegerField(default=100000)),
                ('wallet_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('account_number', models.CharField(max_length=20)),
                ('bank', models.CharField(max_length=20)),
                ('bvn', models.CharField(max_length=11)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
