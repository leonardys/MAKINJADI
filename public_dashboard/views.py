from django.shortcuts import render
from expense_tracker.models import ExpenseDocument


def index(request):
    expense_documents = ExpenseDocument.objects.order_by("date")
    context = {"expense_documents": expense_documents}
    return render(request, "dashboard/index.html", context)
