# Generated by Django 4.2.6 on 2023-10-23 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eid', models.CharField(max_length=18)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('short_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.employee')),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.workorder')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('place', models.CharField(max_length=50)),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.workorder')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.unit'),
        ),
    ]