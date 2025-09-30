from django.urls import path
from .apps import ManageCashConfig
from .views import (TransactionListView,
                    CreateTransactionView,
                    CreateStatusView,
                    CreateTypeView,
                    CreateCategoryView,
                    CreateSubcategoryView,)

app_name = ManageCashConfig.name


urlpatterns = [
    path("", TransactionListView.as_view(), name="home"),
    path("create/", CreateTransactionView.as_view(), name="create_transaction"),
    ############################################################################
    # Работа со справочниками - создание
    path("add_status/", CreateStatusView.as_view(), name="add_status"),
    path("add_type/", CreateTypeView.as_view(), name="add_type"),
    path("add_category/", CreateCategoryView.as_view(), name="add_category"),
    path("add_subcategory/", CreateSubcategoryView.as_view(), name="add_subcategory"),

]