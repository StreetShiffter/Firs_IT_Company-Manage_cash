from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView

from manage_cash.forms import TypeForm
from manage_cash.models import TypeTransaction


class TypeListView(LoginRequiredMixin, ListView):
    """Просмотр всех типов"""

    model = TypeTransaction
    template_name = "manage_cash/list_type.html"
    context_object_name = "types"


class TypeDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление типа категории"""

    model = TypeTransaction
    success_url = reverse_lazy("manage_cash:list_type")
    template_name = "manage_cash/type_confirm_delete.html"

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"Нельзя удалить тип категории «{self.object.name}»: "
                f"с ней связаны категории или транзакции.",
            )
            return redirect(self.success_url)


class TypeUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование названия типа категории"""

    model = TypeTransaction
    form_class = TypeForm
    template_name = "manage_cash/type_form.html"
    success_url = reverse_lazy("manage_cash:list_type")

    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)
