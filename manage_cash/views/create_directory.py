from django.urls import reverse_lazy
from django.views.generic import CreateView
from manage_cash.forms import StatusForm, TypeForm, CategoryForm, SubcategoryForm
from manage_cash.models import StatusTransaction, TypeTransaction, Category, Subcategory


class CreateStatusView(CreateView):
    """Создание записи статуса транзакции"""

    model = StatusTransaction
    form_class = StatusForm
    template_name = "manage_cash/status_form.html"
    success_url = reverse_lazy("manage_cash:list_status")


class CreateTypeView(CreateView):
    """Создание записи типа транзакции"""

    model = TypeTransaction
    form_class = TypeForm
    template_name = "manage_cash/type_form.html"
    success_url = reverse_lazy("manage_cash:list_type")


class CreateCategoryView(CreateView):
    """Создание записи категории транзакции"""

    model = Category
    form_class = CategoryForm
    template_name = "manage_cash/category_form.html"
    success_url = reverse_lazy("manage_cash:list_category")


class CreateSubcategoryView(CreateView):
    """Создание записи подкатегории транзакции"""

    model = Subcategory
    form_class = SubcategoryForm
    template_name = "manage_cash/subcategory_form.html"
    success_url = reverse_lazy("manage_cash:list_subcategory")
