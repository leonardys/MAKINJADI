# Generated by Django 4.2.6 on 2023-11-06 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense_tracker', '0005_rename_place_workday_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Pegawai', 'verbose_name_plural': 'Pegawai'},
        ),
        migrations.AlterModelOptions(
            name='expensedocument',
            options={'verbose_name': 'Surat Perjalanan Dinas (SPD)', 'verbose_name_plural': 'Surat Perjalanan Dinas (SPD)'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name': 'Unit Organisasi', 'verbose_name_plural': 'Unit Organisasi'},
        ),
        migrations.AlterModelOptions(
            name='workday',
            options={'verbose_name': 'Waktu Pelaksanaan Tugas', 'verbose_name_plural': 'Waktu Pelaksanaan Tugas'},
        ),
        migrations.AlterModelOptions(
            name='workorder',
            options={'verbose_name': 'Surat Tugas (ST)', 'verbose_name_plural': 'Surat Tugas (ST)'},
        ),
        migrations.AlterField(
            model_name='employee',
            name='eid',
            field=models.CharField(max_length=18, verbose_name='NIP'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nama Pegawai'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.unit', verbose_name='Unit Organisasi'),
        ),
        migrations.AlterField(
            model_name='expensedocument',
            name='date',
            field=models.DateField(verbose_name='Tanggal SPD'),
        ),
        migrations.AlterField(
            model_name='expensedocument',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.employee', verbose_name='Nama Pegawai'),
        ),
        migrations.AlterField(
            model_name='expensedocument',
            name='number',
            field=models.CharField(max_length=30, verbose_name='Nomor SPD'),
        ),
        migrations.AlterField(
            model_name='expensedocument',
            name='work_days',
            field=models.ManyToManyField(to='expense_tracker.workday', verbose_name='Waktu Pelaksanaan Tugas'),
        ),
        migrations.AlterField(
            model_name='expensedocument',
            name='work_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.workorder', verbose_name='Nomor ST'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='Nama Lengkap'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='short_name',
            field=models.CharField(max_length=30, verbose_name='Nama Pendek'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='date',
            field=models.DateField(verbose_name='Tanggal ST'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='desc',
            field=models.TextField(verbose_name='Deskripsi Penugasan'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='number',
            field=models.CharField(max_length=30, verbose_name='Nomor ST'),
        ),
        migrations.CreateModel(
            name='ExpenseDocumentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ACC', 'Berkas Diterima'), ('NC', 'Berkas Tidak Lengkap'), ('CMPLT', 'Berkas Lengkap'), ('CALC', 'Proses Penghitungan Biaya Perjalanan Dinas'), ('READY', 'Penghitungan Biaya Perjalanan Dinas Selesai'), ('DONE', 'Biaya Perjalanan Dinas Dibayarkan')], max_length=5)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expense_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='expense_tracker.expensedocument', verbose_name='Surat Perjalanan Dinas (SPD)')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Status SPD',
                'verbose_name_plural': 'Status SPD',
            },
        ),
    ]