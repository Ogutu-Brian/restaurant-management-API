# Generated by Django 3.1 on 2020-08-08 21:38

from django.db import migrations, models
import django.db.models.expressions
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_ticket_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.expressions.Case, to='restaurant.ticket')),
            ],
        ),
    ]
