from django.contrib import admin
from django.db import models
from django import forms
from .models import (
    WorkOrder,
    WorkDay,
    ExpenseDocument,
    ExpenseDocumentLog,
    Unit,
    Employee,
    ExpenseType,
    Expense,
    PaymentBundle,
)


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1


class WorkDayInline(admin.TabularInline):
    model = WorkDay
    extra = 1
    formfield_overrides = {
        models.TimeField: {"widget": forms.TimeInput(format="%H:%M")},
    }


class ExpenseDocumentInline(admin.TabularInline):
    model = ExpenseDocument
    exclude = ["work_days"]
    extra = 1


class ExpenseDocumentLogInline(admin.TabularInline):
    model = ExpenseDocumentLog
    exclude = ["user"]
    extra = 1
    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 4, "cols": 60})},
    }

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def get_max_num(self, request, obj):
        if obj:
            return obj.logs.count() + 1
        return 1


class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ["number", "date", "num_of_employees", "num_of_days"]
    ordering = ["number"]
    inlines = [WorkDayInline, ExpenseDocumentInline]

    class Media:
        css = {"all": ["expense_tracker/hide.css"]}


class ExpenseDocumentAdmin(admin.ModelAdmin):
    fields = ("work_order", "number", "date", "employee", "work_days")
    list_display = [
        "number",
        "date",
        "employee",
        "range_of_work_days",
        "last_status",
        "last_update",
    ]
    ordering = ["-date"]
    inlines = [ExpenseDocumentLogInline, ExpenseInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["work_days"].queryset = WorkDay.objects.filter(
                work_order_id=obj.work_order_id
            )
        return form

    def get_readonly_fields(self, request, obj):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields = (*readonly_fields, "work_order")
        return readonly_fields

    def has_add_permission(self, request):
        return False

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    class Media:
        css = {"all": ["expense_tracker/hide.css"]}


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "unit"]
    ordering = ["name"]


class UnitAdmin(admin.ModelAdmin):
    ordering = ["full_name"]

    def has_module_permission(self, request):
        return False


class ExpenseTypeAdmin(admin.ModelAdmin):
    ordering = ["name"]

    def has_module_permission(self, request):
        return False


admin.site.site_header = "MAKINJADI"
admin.site.site_title = "Manajemen Keuangan dan Informasi Perjalanan Dinas (MAKINJADI)"

admin.site.register(ExpenseDocument, ExpenseDocumentAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(ExpenseType, ExpenseTypeAdmin)
admin.site.register(PaymentBundle)
