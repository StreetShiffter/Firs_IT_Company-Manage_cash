from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView

from manage_cash.forms import StatusForm
from manage_cash.models import StatusTransaction


class StatusListView(LoginRequiredMixin, ListView):
    """Просмотр всех статусов транзакции"""

    model = StatusTransaction
    template_name = "manage_cash/list_status.html"
    context_object_name = "statuses"


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление статуса транзакции"""

    model = StatusTransaction
    success_url = reverse_lazy("manage_cash:list_type")
    template_name = "manage_cash/status_confirm_delete.html"

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"Нельзя удалить статус «{self.object.name}»: "
                f"с ней связаны транзакции.",
            )
            return redirect(self.success_url)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование названия статуса"""

    model = StatusTransaction
    form_class = StatusForm
    template_name = "manage_cash/status_form.html"
    success_url = reverse_lazy("manage_cash:list_status")

    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)
