from django.views import generic
from expense_tracker.models import ExpenseDocument
from django.db import models


class IndexView(generic.ListView):
    template_name = "dashboard/index.html"
    context_object_name = "expense_documents"

    def get_queryset(self):
        return ExpenseDocument.objects.annotate(
            last_status_update=models.Max("logs__created_at")
        ).order_by("-last_status_update", "date", "work_order__number")


class DetailView(generic.DetailView):
    template_name = "dashboard/detail.html"
    context_object_name = "expense_document"
    queryset = ExpenseDocument.objects.all()
