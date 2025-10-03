from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView

from manage_cash.forms import CategoryForm
from manage_cash.models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """Просмотр всех категорий"""

    model = Category
    template_name = "manage_cash/list_category.html"
    context_object_name = "categories"


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление категории"""

    model = Category
    success_url = reverse_lazy("manage_cash:list_category")
    template_name = "manage_cash/category_confirm_delete.html"

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"Нельзя удалить категорию «{self.object.name}»: "
                f"с ней связаны подкатегории или транзакции.",
            )
            return redirect(self.success_url)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование названия категории"""

    model = Category
    form_class = CategoryForm
    template_name = "manage_cash/category_form.html"
    success_url = reverse_lazy("manage_cash:list_category")

    def form_valid(self, form):
        if self.request.user.is_superuser:
            return super().form_valid(form)
