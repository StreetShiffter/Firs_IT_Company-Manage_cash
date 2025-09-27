from django.urls import path
from . import views
from .apps import ManageCashConfig

app_name = ManageCashConfig.name

urlpatterns = [
    path("", views.home_view, name="home"),]