from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from manage_cash.models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """Просмотр всех категорий"""

    model = Category
    template_name = "manage_cash/list_category.html"
    context_object_name = "categories"


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление категории"""
    model = Category
    success_url = reverse_lazy('manage_cash:list_category')
    template_name = 'manage_cash/category_confirm_delete.html'

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"Нельзя удалить категорию «{self.object.name}»: "
                f"с ней связаны подкатегории или транзакции."
            )
            return redirect(self.success_url)