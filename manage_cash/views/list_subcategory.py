from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView

from manage_cash.forms import SubcategoryForm
from manage_cash.models import Subcategory


class SubcategoryListView(LoginRequiredMixin, ListView):
    """Просмотр всех подкатегорий"""

    model = Subcategory
    template_name = "manage_cash/list_subcategory.html"
    context_object_name = "subcategories"


class SubcategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление подкатегории"""

    model = Subcategory
    success_url = reverse_lazy("manage_cash:list_subcategory")
    template_name = "manage_cash/subcategory_confirm_delete.html"

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"Нельзя удалить подкатегорию «{self.object.name}»: "
                f"с ней связаны категории или транзакции.",
            )
            return redirect(self.success_url)


class SubcategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование названия подкатегории"""

    model = Subcategory
    form_class = SubcategoryForm
    template_name = "manage_cash/subcategory_form.html"
    success_url = reverse_lazy("manage_cash:list_subcategory")

    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)
