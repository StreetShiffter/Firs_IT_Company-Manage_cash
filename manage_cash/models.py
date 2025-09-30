from datetime import date
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User

class TypeTransaction(models.Model):
    """Модель списка транзакции"""
    name = models.CharField(max_length=100, verbose_name='Тип транзакции')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип транзакции'
        verbose_name_plural = 'Типы транзакции'


class StatusTransaction(models.Model):
    """Модель списка статусов"""
    name = models.CharField(max_length=100, verbose_name='Статус')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

class Category(models.Model):
    """Модель списка категории"""
    name = models.CharField(max_length=100, verbose_name='Категория')
    transaction_type = models.ForeignKey(
        TypeTransaction,
        on_delete=models.PROTECT,
        related_name='categories',
        verbose_name='Тип транзакции'
    )
    def __str__(self):
        return f'{self.name}, {self.transaction_type}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ('name',
                           'transaction_type')# Сохранение уникальности категории в готовом типе


class Subcategory(models.Model):
    """Модель списка подкатегории
    (ссылка на категорию с защитой от удаления если есть записи в ней)"""
    name = models.CharField(max_length=100, verbose_name='Подкатегория')
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='subcategories',
                                 verbose_name='Категория')

    def __str__(self):
        return f'{self.name}, {self.category}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Transaction(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='transaction',
                              verbose_name='Транзакции пользователя',)
    status = models.ForeignKey(StatusTransaction,
                               on_delete = models.PROTECT,
                               related_name='transactions',
                               verbose_name='Cтатус транзакции')
    type = models.ForeignKey(TypeTransaction,
                               on_delete=models.PROTECT,
                               related_name='transactions',
                               verbose_name='Тип транзакции')
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='transactions',
                                 verbose_name='Категория транзакции')
    subcategory = models.ForeignKey(Subcategory,
                                 on_delete=models.PROTECT,
                                 related_name='transactions',
                                 verbose_name='Подкатегория транзакции')
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Сумма оплаты",)
    comment = models.CharField(max_length = 150,
                               verbose_name = "Комментарий",
                               blank = True,
                               null = True)
    date = models.DateField(verbose_name="Дата операции",
                            default=date.today)

# Валидность данных - если обращаться по API, игнорируя фронт
    def clean(self):
        """Метод проверки условий"""
        super().clean()
        # Связь категории и типа
        if self.category_id:  #Проверяем ID
            if not self.type:
                raise ValidationError({'type': 'Тип транзакции обязателен при выборе категории.'})
            if self.category.transaction_type != self.type:  # Только если category существует
                raise ValidationError({'category': 'Категория не соответствует типу транзакции.'})

        # Связь категории и подкатегории
        if self.subcategory_id:
            if not self.category_id:
                raise ValidationError({'subcategory': 'Нельзя выбрать подкатегорию без категории.'})
            if self.subcategory.category != self.category:
                raise ValidationError({'subcategory': 'Подкатегория не соответствует категории.'})

    def save(self, *args, **kwargs):
        """Метод сохранения для предотвращения работы данных через API"""
        self.full_clean()  # вызывает clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner} {self.comment}'

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['status', 'type', "category", "subcategory", "-date"]
        # permissions = [
        #     ("can_unpublish_product", "Может отменять публикацию продукта"),
        # ]