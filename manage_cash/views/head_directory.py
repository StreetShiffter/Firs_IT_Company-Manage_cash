from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DeleteView

from manage_cash.forms import (
    TransactionForm,
    StatusForm,
    TypeForm,
    CategoryForm,
    SubcategoryForm,
)
from manage_cash.models import (
    Transaction,
    StatusTransaction,
    TypeTransaction,
    Category,
    Subcategory,
)


class CreateTransactionView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "manage_cash/transaction_form.html"
    success_url = reverse_lazy("manage_cash:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TransactionListView(ListView):
    """Просмотр всех записей транзакций - главная"""

    model = Transaction
    template_name = "manage_cash/home.html"
    context_object_name = "transactions"

    # paginate_by = 20  # опционально: пагинация

    def get_queryset(self):
        queryset = Transaction.objects.all()

        # Фильтрация
        if start_date := self.request.GET.get("start_date"):
            queryset = queryset.filter(date__gte=start_date)
        if end_date := self.request.GET.get("end_date"):
            queryset = queryset.filter(date__lte=end_date)
        if status_id := self.request.GET.get("status"):
            queryset = queryset.filter(status_id=status_id)
        if type_id := self.request.GET.get("type"):
            queryset = queryset.filter(type_id=type_id)
        if category_id := self.request.GET.get("category"):
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id := self.request.GET.get("subcategory"):
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаём справочники для выпадающих списков
        context["statuses"] = StatusTransaction.objects.all()
        context["types"] = TypeTransaction.objects.all()
        context["categories"] = Category.objects.all()
        context["subcategories"] = Subcategory.objects.all()
        return context


class CreateAllDirectoryView(LoginRequiredMixin, TemplateView):
    """Страница работы со справочниками"""

    template_name = "manage_cash/all_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_form"] = StatusForm()
        context["type_form"] = TypeForm()
        context["category_form"] = CategoryForm()
        context["subcategory_form"] = SubcategoryForm()
        return context


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """Позволить удалять транзакции админу и пользователю по правам"""

    model = Transaction
    success_url = reverse_lazy("manage_cash:home")
    template_name = "manage_cash/transaction_confirm_delete.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs  # Админ видит все
        return qs.filter(owner=self.request.user)
