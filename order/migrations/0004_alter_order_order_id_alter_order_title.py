# Generated by Django 5.1.1 on 2024-09-20 13:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_khalti_txn_id_order_pidx_alter_order_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='title',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
