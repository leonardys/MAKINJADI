# Generated by Django 4.2.6 on 2023-10-24 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker', '0003_workorder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='unit',
            name='short_name',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='ExpenseDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.employee')),
                ('work_days', models.ManyToManyField(to='expense_tracker.workday')),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.workorder')),
            ],
        ),
    ]
