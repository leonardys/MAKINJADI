from django.db import models
from django.db.models import Sum
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


class PaymentBundle(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Bundel")

    def __str__(self):
        return self.name

    def document_count(self):
        return self.documents.count()

    def total_expense(self):
        return self.documents.aggregate(total=Sum("expenses__amount"))["total"]

    class Meta:
        verbose_name_plural = verbose_name = "Bundel"

    total_expense.short_description = "Jumlah Biaya"
    document_count.short_description = "Jumlah SPD"


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
    payment_bundle = models.ForeignKey(
        PaymentBundle,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Bundel",
        related_name="documents",
    )

    def __str__(self):
        return self.number

    def last_status(self):
        if self.logs.count():
            return self.logs.order_by("-created_at")[0].status_label()
        return "Menunggu Berkas"

    def last_update(self):
        if self.logs.count():
            return self.logs.order_by("-created_at")[0].created_at
        return ""

    def total_expense(self):
        return self.expenses.aggregate(total=Sum("amount"))["total"]

    class Meta:
        verbose_name_plural = verbose_name = "Surat Perjalanan Dinas (SPD)"

    last_status.short_description = "Status"
    last_update.short_description = "Tanggal Update"
    total_expense.short_description = "Jumlah Biaya"


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

    def status_label(self):
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
    expense_document = models.ForeignKey(
        ExpenseDocument, on_delete=models.CASCADE, related_name="expenses"
    )
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
