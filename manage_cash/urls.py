from django.urls import path
from .apps import ManageCashConfig
from .views import TransactionListView, CreateTransactionView

app_name = ManageCashConfig.name

urlpatterns = [
    path("", TransactionListView.as_view(), name="home"),
    path("create/", CreateTransactionView.as_view(), name="create_transaction"),]