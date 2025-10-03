from django.urls import path
from .apps import ManageCashConfig
from .views import (
    TransactionListView,
    CreateTransactionView,
    CreateStatusView,
    CreateTypeView,
    CreateCategoryView,
    CreateSubcategoryView,
    get_types_ajax,
    add_status_ajax,
    add_type_ajax,
    add_category_ajax,
    add_subcategory_ajax,
    get_categories_by_type,
    get_subcategories_by_category,
    CategoryListView,
    CategoryDeleteView,
    StatusListView,
    StatusDeleteView,
)
from .views.AJAX_module import transaction_update_ajax

from .views.head_directory import CreateAllDirectoryView, TransactionDeleteView
from .views.list_category import CategoryUpdateView
from .views.list_status import StatusUpdateView
from .views.list_subcategory import (
    SubcategoryListView,
    SubcategoryDeleteView,
    SubcategoryUpdateView,
)
from .views.list_type import TypeListView, TypeDeleteView, TypeUpdateView

app_name = ManageCashConfig.name


urlpatterns = [
    path("", TransactionListView.as_view(), name="home"),
    path("create/", CreateTransactionView.as_view(), name="create_transaction"),
    path(
        "transaction/delete/<int:pk>/",
        TransactionDeleteView.as_view(),
        name="transaction_confirm_delete",
    ),
    path("directory/", CreateAllDirectoryView.as_view(), name="create_directory"),
    ############################################################################
    # Работа со справочниками - создание
    path("add_status/", CreateStatusView.as_view(), name="add_status"),
    path("add_type/", CreateTypeView.as_view(), name="add_type"),
    path("add_category/", CreateCategoryView.as_view(), name="add_category"),
    path("add_subcategory/", CreateSubcategoryView.as_view(), name="add_subcategory"),
    # Работа со справочниками - просмотр списка и удаление
    path("list_category/", CategoryListView.as_view(), name="list_category"),
    path(
        "category/delete/<int:pk>/",
        CategoryDeleteView.as_view(),
        name="category_confirm_delete",
    ),
    path("list_subcategory/", SubcategoryListView.as_view(), name="list_subcategory"),
    path(
        "subcategory/delete/<int:pk>/",
        SubcategoryDeleteView.as_view(),
        name="subcategory_confirm_delete",
    ),
    path("list_type/", TypeListView.as_view(), name="list_type"),
    path("type/delete/<int:pk>/", TypeDeleteView.as_view(), name="type_confirm_delete"),
    path("list_status/", StatusListView.as_view(), name="list_status"),
    path(
        "status/delete/<int:pk>/",
        StatusDeleteView.as_view(),
        name="status_confirm_delete",
    ),
    path("status/<int:pk>/edit/", StatusUpdateView.as_view(), name="status_edit"),
    path("type/<int:pk>/edit/", TypeUpdateView.as_view(), name="type_edit"),
    path("category/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path(
        "subcategory/<int:pk>/edit/",
        SubcategoryUpdateView.as_view(),
        name="subcategory_edit",
    ),
    # AJAX-эндпоинты для модальных окон  #########################################################
    path("ajax/types/", get_types_ajax, name="get_types_ajax"),
    path("ajax/categories/", get_categories_by_type, name="get_categories_by_type"),
    path(
        "ajax/subcategories/",
        get_subcategories_by_category,
        name="get_subcategories_by_category",
    ),
    path("ajax/add_status/", add_status_ajax, name="add_status_ajax"),
    path("ajax/add_type/", add_type_ajax, name="add_type_ajax"),
    path("ajax/add_category/", add_category_ajax, name="add_category_ajax"),
    path("ajax/add_subcategory/", add_subcategory_ajax, name="add_subcategory_ajax"),
    path(
        "ajax/transaction/update/",
        transaction_update_ajax,
        name="transaction_update_ajax",
    ),
]
