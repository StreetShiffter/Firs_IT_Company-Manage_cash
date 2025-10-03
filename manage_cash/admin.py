from django.contrib import admin
from .models import (
    Category,
    Subcategory,
    TypeTransaction,
    StatusTransaction,
    Transaction,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "transaction_type")
    search_fields = ("name",)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name",)


@admin.register(TypeTransaction)
class TypeTransactionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(StatusTransaction)
class StatusTransactionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "status",
        "date",
        "amount",
        "category",
        "subcategory",
        "type",
        "comment",
    )
    search_fields = (
        "owner",
        "status",
        "date",
        "amount",
        "category",
        "subcategory",
        "type",
    )
