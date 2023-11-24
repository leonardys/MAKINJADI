from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    short_name = models.CharField(max_length=30, verbose_name="Nama Pendek")

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name_plural = verbose_name = "Unit Organisasi"


class Employee(models.Model):
    eid = models.CharField(max_length=18, verbose_name="NIP")
    name = models.CharField(max_length=100, verbose_name="Nama Pegawai")
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, verbose_name="Unit Organisasi"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "Pegawai"


class WorkOrder(models.Model):
    number = models.CharField(max_length=30, verbose_name="Nomor ST")
    date = models.DateField(verbose_name="Tanggal ST")
    desc = models.TextField(verbose_name="Deskripsi Penugasan")

    def __str__(self):
        return self.number

    def num_of_days(self):
        return self.workday_set.count()

    def num_of_employees(self):
        return self.expensedocument_set.count()

    class Meta:
        verbose_name_plural = verbose_name = "Surat Tugas (ST)"

    num_of_days.short_description = "Jumlah Hari"
    num_of_employees.short_description = "Jumlah Pegawai"


class WorkDay(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=50)

    def __str__(self):
        return "{date} ({start_time}-{end_time})".format(
            date=self.date,
            start_time=self.start_time.strftime("%H:%M"),
            end_time=self.end_time.strftime("%H:%M"),
        )

    class Meta:
        verbose_name_plural = verbose_name = "Waktu Pelaksanaan Tugas"


class ExpenseDocument(models.Model):
    work_order = models.ForeignKey(
        WorkOrder, on_delete=models.CASCADE, verbose_name="Nomor ST"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Nama Pegawai"
    )
    work_days = models.ManyToManyField(WorkDay, verbose_name="Waktu Pelaksanaan Tugas")
    number = models.CharField(max_length=30, verbose_name="Nomor SPD")
    date = models.DateField(verbose_name="Tanggal SPD")

    def __str__(self):
        return self.number

    def range_of_work_days(self):
        if self.work_days.count() > 1:
            return "{} s.d. {}".format(
                self.work_days.order_by("date")[0].date.strftime("%Y-%m-%d"),
                self.work_days.order_by("-date")[0].date.strftime("%Y-%m-%d"),
            )
        elif self.work_days.count() == 1:
            return "{}".format(self.work_days.order_by("date")[0].date)
        else:
            return "Waktu Pelaksanaan Belum Diatur"

    def last_status(self):
        if self.logs.count():
            return self.logs.order_by("-created_at")[0].get_status()
        return "Menunggu Berkas"

    def last_update(self):
        if self.logs.count():
            return self.logs.order_by("-created_at")[0].created_at.strftime(
                "%Y-%m-%d %H:%S"
            )
        return ""

    class Meta:
        verbose_name_plural = verbose_name = "Surat Perjalanan Dinas (SPD)"

    range_of_work_days.short_description = "Waktu Pelaksanaan"
    last_status.short_description = "Status Terakhir"
    last_update.short_description = "Tanggal Update"


class ExpenseDocumentLog(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = ("SUBMITTED", "Berkas Diterima")
        NOT_COMPLETE = ("NOT_COMPLETE", "Berkas Tidak Lengkap")
        IN_CALCULATION = ("IN_CALCULATION", "Berkas Lengkap, Proses Penghitungan")
        CALCULATION_COMPLETED = (
            "CALCULATION_COMPLETED",
            "Penghitungan Selesai, Berkas Diserahkan ke Bendahara",
        )
        FINAL_VERIFICATION = ("FINAL_VERIFICATION", "Proses Verifikasi")
        READY_FOR_PAYMENT = ("READY_FOR_PAYMENT", "Siap Dibayarkan")
        DONE = ("DONE", "Selesai Dibayarkan")

    expense_document = models.ForeignKey(
        ExpenseDocument,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
    )
    note = models.TextField(blank=True, verbose_name="Catatan")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_status(self):
        return self.Status(self.status).label

    class Meta:
        verbose_name_plural = verbose_name = "Status SPD"


class ExpenseType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Jenis Biaya Perjalanan Dinas")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "Jenis Biaya Perjalanan Dinas"


class Expense(models.Model):
    expense_document = models.ForeignKey(ExpenseDocument, on_delete=models.CASCADE)
    type = models.ForeignKey(
        ExpenseType,
        on_delete=models.CASCADE,
        verbose_name="Jenis Biaya Perjalanan Dinas",
    )
    amount = models.PositiveIntegerField(verbose_name="Nilai")

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name_plural = verbose_name = "Biaya Perjalanan Dinas"
