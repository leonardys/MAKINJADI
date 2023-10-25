from django.contrib import admin
from django.http.request import HttpRequest

from .models import WorkOrder, WorkDay, ExpenseDocument, Unit, Employee


class WorkDayInline(admin.TabularInline):
    model = WorkDay
    extra = 1


class ExpenseDocumentInline(admin.TabularInline):
    model = ExpenseDocument
    exclude = ["work_days"]
    extra = 1


class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ["number", "date", "num_of_employees", "num_of_days"]
    ordering = ["number"]
    inlines = [WorkDayInline, ExpenseDocumentInline]


class ExpenseDocumentAdmin(admin.ModelAdmin):
    list_display = ["number", "date", "employee", "num_of_days"]
    ordering = ["-date"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:
            form.base_fields["work_days"].queryset = WorkDay.objects.filter(
                work_order_id=obj.work_order_id
            )
        return form

    def has_add_permission(self, request):
        return False


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "unit"]
    ordering = ["name"]


class UnitAdmin(admin.ModelAdmin):
    list_display = ["full_name", "short_name"]
    ordering = ["full_name"]


admin.site.register(ExpenseDocument, ExpenseDocumentAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Employee, EmployeeAdmin)
