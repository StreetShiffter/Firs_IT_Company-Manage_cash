# manage_cash/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView

from manage_cash.forms import TransactionForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from manage_cash.models import Transaction, StatusTransaction, TypeTransaction, Category, Subcategory




class CreateTransactionView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "manage_cash/transaction_form.html"
    success_url = reverse_lazy("manage_cash:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateStatusView(CreateView):
    """Создание записи статуса транзакции"""
    model = StatusTransaction
    form_class = StatusForm
    template_name = "manage_cash/status_form.html"
    success_url = reverse_lazy("manage_cash:create_transaction")


class CreateTypeView(CreateView):
    """Создание записи типа транзакции"""
    model = TypeTransaction
    form_class = TypeForm
    template_name = "manage_cash/type_form.html"
    success_url = reverse_lazy("manage_cash:create_transaction")


class CreateCategoryView(CreateView):
    """Создание записи категории транзакции"""
    model = Category
    form_class = CategoryForm
    template_name = "manage_cash/category_form.html"
    success_url = reverse_lazy("manage_cash:create_transaction")


class CreateSubcategoryView(CreateView):
    """Создание записи подкатегории транзакции"""
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "manage_cash/subcategory_form.html"
    success_url = reverse_lazy("manage_cash:create_transaction")



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

#ВЬЮШКИ ДЛЯ МОДАЛЬНЫХ ОКОН в заполнении формы транзакции
def get_types_ajax(request):
    """AJAX: получить все типы транзакций для модального окна"""
    types = TypeTransaction.objects.values('id', 'name')
    return JsonResponse(list(types), safe=False)

def get_categories_by_type(request):
    """AJAX: получить категории для выбранного типа"""
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(transaction_type_id=type_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)

def get_subcategories_by_category(request):
    """AJAX: получить подкатегории для выбранной категории"""
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def add_status_ajax(request):
    form = StatusForm(request.POST)
    if form.is_valid():
        status = form.save()
        return JsonResponse({
            'success': True,
            'item': {
                'id': status.id,
                'name': status.name
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'error': form.errors.as_json()
        })

@csrf_exempt
@require_http_methods(["POST"])
def add_type_ajax(request):
    form = TypeForm(request.POST)
    if form.is_valid():
        type_obj = form.save()
        return JsonResponse({
            'success': True,
            'item': {
                'id': type_obj.id,
                'name': type_obj.name
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'error': form.errors.as_json()
        })

@csrf_exempt
@require_http_methods(["POST"])
def add_category_ajax(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = form.save()
        return JsonResponse({
            'success': True,
            'item': {
                'id': category.id,
                'name': category.name
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'error': form.errors.as_json()
        })

@csrf_exempt
@require_http_methods(["POST"])
def add_subcategory_ajax(request):
    form = SubcategoryForm(request.POST)
    if form.is_valid():
        subcategory = form.save()
        return JsonResponse({
            'success': True,
            'item': {
                'id': subcategory.id,
                'name': subcategory.name
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'error': form.errors.as_json()
        })