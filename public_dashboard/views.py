from django.views import generic
from expense_tracker.models import ExpenseDocument
from django.db.models import Max


class IndexView(generic.ListView):
    model = ExpenseDocument
    template_name = "dashboard/index.html"
    context_object_name = "expense_documents"

    def get_queryset(self):
        return ExpenseDocument.objects.annotate(
            last_status_update=Max("logs__created_at")
        ).order_by("-last_status_update", "date", "work_order__number")
