# Generated by Django 4.2.6 on 2023-12-04 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker', '0012_alter_expense_options_alter_expensetype_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentBundle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nama Bundel')),
            ],
            options={
                'verbose_name': 'Bundel',
                'verbose_name_plural': 'Bundel',
            },
        ),
        migrations.AddField(
            model_name='expensedocument',
            name='payment_bundle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='expense_tracker.paymentbundle', verbose_name='Bundel'),
        ),
    ]
