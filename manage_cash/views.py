# manage_cash/views.py
from django.shortcuts import render
from django.views.generic import CreateView

from manage_cash.models import Transaction, StatusTransaction, TypeTransaction, Category, Subcategory

def home_view(request):
    """Главная страница с записями и фильтрацией"""
    queryset = Transaction.objects.all()
    # Сортировка
    # sort_params = ['status', 'type', 'category', 'subcategory', 'date', '-date']
    # sort_fields = []
    #
    # for param in sort_params:
    #     if param in request.GET:
    #         sort_fields.append(param)
    #
    # # Если ничего не выбрано — сортируем по умолчанию
    # if not sort_fields:
    #     sort_fields = ['-date']
    #
    # transactions = queryset.order_by(*sort_fields)

    # Фильтрация по всем полям
    if start_date := request.GET.get('start_date'):
        queryset = queryset.filter(date__gte=start_date)
    if end_date := request.GET.get('end_date'):
        queryset = queryset.filter(date__lte=end_date)
    if status_id := request.GET.get('status'):
        queryset = queryset.filter(status_id=status_id)
    if type_id := request.GET.get('type'):
        queryset = queryset.filter(type_id=type_id)
    if category_id := request.GET.get('category'):
        queryset = queryset.filter(category_id=category_id)
    if subcategory_id := request.GET.get('subcategory'):
        queryset = queryset.filter(subcategory_id=subcategory_id)

    # Передаём справочники в шаблон для выпадающих списков
    context = {
        'transactions': queryset,
        'statuses': StatusTransaction.objects.all(),
        'types': TypeTransaction.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }
    return render(request, 'manage_cash/home.html', context)
