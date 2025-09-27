# manage_cash/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from manage_cash.forms import TransactionForm
from manage_cash.models import Transaction, StatusTransaction, TypeTransaction, Category, Subcategory


class CreateTransactionView(CreateView):
    """Создание записи транзакции"""
    model = Transaction
    form_class = TransactionForm
    template_name = "manage_cash/transaction_form.html"
    success_url = reverse_lazy("transaction:home")

    def form_valid(self, form):
        """Добавим к записи авторизованного владельца"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TransactionListView(ListView):
    """Просмотр всех записей транзакций - главная"""

    model = Transaction
    template_name = 'manage_cash/home.html'
    context_object_name = 'transactions'

    # paginate_by = 20  # опционально: пагинация

    def get_queryset(self):
        queryset = Transaction.objects.all()

        # Фильтрация
        if start_date := self.request.GET.get('start_date'):
            queryset = queryset.filter(date__gte=start_date)
        if end_date := self.request.GET.get('end_date'):
            queryset = queryset.filter(date__lte=end_date)
        if status_id := self.request.GET.get('status'):
            queryset = queryset.filter(status_id=status_id)
        if type_id := self.request.GET.get('type'):
            queryset = queryset.filter(type_id=type_id)
        if category_id := self.request.GET.get('category'):
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id := self.request.GET.get('subcategory'):
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаём справочники для выпадающих списков
        context['statuses'] = StatusTransaction.objects.all()
        context['types'] = TypeTransaction.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context
