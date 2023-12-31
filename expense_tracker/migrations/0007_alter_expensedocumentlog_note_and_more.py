# Generated by Django 4.2.6 on 2023-11-23 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker', '0006_alter_employee_options_alter_expensedocument_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensedocumentlog',
            name='note',
            field=models.TextField(blank=True, verbose_name='Catatan'),
        ),
        migrations.AlterField(
            model_name='expensedocumentlog',
            name='status',
            field=models.CharField(choices=[('ACC', 'Berkas Diterima'), ('NC', 'Berkas Tidak Lengkap'), ('CALC', 'Berkas Diterima Lengkap, Proses Penghitungan'), ('CMPLT', 'Penghitungan Selesai, Berkas Diserahkan ke Bendahara'), ('VRFY', 'Proses Verifikasi'), ('READY', 'Siap Dibayarkan'), ('DONE', 'Biaya Perjalanan Dinas Dibayarkan')], max_length=5),
        ),
    ]
