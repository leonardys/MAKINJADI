from django.db import models


class Unit(models.Model):
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)

    def __str__(self):
        return self.short_name


class Employee(models.Model):
    eid = models.CharField(max_length=18)
    name = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkOrder(models.Model):
    number = models.CharField(max_length=30)
    date = models.DateField()
    desc = models.TextField()

    def __str__(self):
        return self.number

    def num_of_days(self):
        return self.workday_set.count()

    def num_of_employees(self):
        return self.expensedocument_set.count()


class WorkDay(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place = models.CharField(max_length=50)

    def __str__(self):
        return "{date} ({number})".format(date=self.date, number=self.work_order.number)


class ExpenseDocument(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work_days = models.ManyToManyField(WorkDay)
    number = models.CharField(max_length=30)
    date = models.DateField()

    def __str__(self):
        return "{number}: {employee_name}".format(
            number=self.number, employee_name=self.employee.name
        )

    def num_of_days(self):
        return self.work_days.count()
