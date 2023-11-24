# Generated by Django 4.2.6 on 2023-11-24 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker', '0010_expensetype_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensedocumentlog',
            name='expense_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='expense_tracker.expensedocument'),
        ),
    ]