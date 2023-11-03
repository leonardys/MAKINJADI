from django.shortcuts import render
from django.views import generic
from expense_tracker.models import ExpenseDocument


class IndexView(generic.ListView):
    model = ExpenseDocument
    template_name = "dashboard/index.html"
    context_object_name = "expense_documents"

    def get_queryset(self):
        return ExpenseDocument.objects.order_by("date")
