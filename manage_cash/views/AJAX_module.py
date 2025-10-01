#ВЬЮШКИ ДЛЯ МОДАЛЬНЫХ ОКОН в заполнении формы транзакции
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from manage_cash.forms import StatusForm, TypeForm, CategoryForm, SubcategoryForm
from manage_cash.models import Category, TypeTransaction, Subcategory


def get_types_ajax(request):
    """AJAX: получить все типы транзакций для модального окна"""
    types = TypeTransaction.objects.values('id', 'name')
    return JsonResponse(list(types), safe=False)

def get_categories_by_type(request):
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(transaction_type_id=type_id).values('id', 'name')
    else:
        categories = Category.objects.all().values('id', 'name')  # ← все категории
    return JsonResponse(list(categories), safe=False)

def get_subcategories_by_category(request):
    """AJAX: получить подкатегории для выбранной категории"""
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)

# Ответ данных обратно на сервер для модальных окон
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