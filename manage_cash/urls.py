from django.urls import path
from .apps import ManageCashConfig
from .views import (TransactionListView,
                    CreateTransactionView,
                    CreateStatusView,
                    CreateTypeView,
                    CreateCategoryView,
                    CreateSubcategoryView, get_types_ajax, add_status_ajax, add_type_ajax,
                    add_category_ajax, add_subcategory_ajax, get_categories_by_type, get_subcategories_by_category, )

from .views.head_directory import CreateAllDirectoryView

app_name = ManageCashConfig.name


urlpatterns = [
    path("", TransactionListView.as_view(), name="home"),
    path("create/", CreateTransactionView.as_view(), name="create_transaction"),
    path("directory/", CreateAllDirectoryView.as_view(), name="create_directory"),
    ############################################################################
    # Работа со справочниками - создание
    path("add_status/", CreateStatusView.as_view(), name="add_status"),
    path("add_type/", CreateTypeView.as_view(), name="add_type"),
    path("add_category/", CreateCategoryView.as_view(), name="add_category"),
    path("add_subcategory/", CreateSubcategoryView.as_view(), name="add_subcategory"),
    # AJAX-эндпоинты для модальных окон  #########################################################
    path("ajax/types/", get_types_ajax, name="get_types_ajax"),
    path("ajax/categories/", get_categories_by_type, name="get_categories_by_type"),
    path("ajax/subcategories/", get_subcategories_by_category, name="get_subcategories_by_category"),
    path("ajax/add_status/", add_status_ajax, name="add_status_ajax"),
    path("ajax/add_type/", add_type_ajax, name="add_type_ajax"),
    path("ajax/add_category/", add_category_ajax, name="add_category_ajax"),
    path("ajax/add_subcategory/", add_subcategory_ajax, name="add_subcategory_ajax"),


]