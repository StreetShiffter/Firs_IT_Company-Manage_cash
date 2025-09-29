from django import forms
from django.core.exceptions import ValidationError
from manage_cash.models import Transaction, StatusTransaction, TypeTransaction, Category, Subcategory


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status', 'type', 'category', 'subcategory', 'amount', 'comment', 'date']
        # labels = {
        #     'status': 'Статус',
        #     'type': 'Тип',
        #     'category': 'Категория',
        #     'subcategory': 'Подкатегория',
        #     'amount': 'Сумма оплаты',
        #     'comment': 'Комментарий',
        #     'date': 'Дата операции',
        # }

    def __init__(self, *args, **kwargs):
        # Извлекаем type_id и category_id из kwargs, если они есть
        self.type_id = kwargs.pop('type_id', None)
        self.category_id = kwargs.pop('category_id', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Статус транзакции'})

        self.fields['type'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Тип транзакции'})

        # Фильтруем категории по типу
        if self.type_id:
            self.fields['category'].queryset = Category.objects.filter(transaction_type_id=self.type_id)
        else:
            # Если тип не выбран, оставляем пустой список
            self.fields['category'].queryset = Category.objects.none()

        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Категория транзакции (зависит от типа транзакции)'})

        # Фильтруем подкатегории по категории
        if self.category_id:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=self.category_id)
        else:
            # Если категория не выбрана, оставляем пустой список
            self.fields['subcategory'].queryset = Subcategory.objects.none()

        self.fields['subcategory'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подкатегория транзакции (зависит от категории транзакции)'})

        self.fields['amount'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Сумма транзакции'})

        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Комментарий(не обязательно)'})

        self.fields['date'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Дата (оставить пустым для авто заполнения на момент создания)'})
        self.fields['date'].required = False


    def clean_amount(self):
        """Валидатор корректной суммы"""
        amount = self.cleaned_data.get('amount')
        if amount < 0:
            raise ValidationError('Сумма не может быть отрицательной!')
        elif amount == 0:
            raise ValidationError('Сумма не может нулевой!')
        return amount

    # Опционально: Добавим валидацию связей
    def clean_category(self):
        category = self.cleaned_data.get('category')
        type_cat = self.cleaned_data.get('type')

        if category and type_cat:
            if category.transaction_type != type_cat:
                raise ValidationError('Выбранная категория не соответствует выбранному типу транзакции.')

        return category

    def clean_subcategory(self):
        subcategory = self.cleaned_data.get('subcategory')
        category = self.cleaned_data.get('category')

        if subcategory and category:
            if subcategory.category != category:
                raise ValidationError('Выбранная подкатегория не соответствует выбранной категории.')

        return subcategory

#Создание справочников
class StatusForm(forms.ModelForm):
    """Форма статуса транзакции"""
    class Meta:
        model = StatusTransaction
        fields = ['name']

    def clean_name(self):
        """Валидатор проверяющий наличие похожего статуса"""
        name = self.cleaned_data.get('name')
        if name:
            cleaned_name = name.lower().strip()
            existing = StatusTransaction.objects.filter(name__iexact=cleaned_name)
            # Проверка редактирования
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            # Если форма редактирует существующий объект
            if existing.exists():
                raise ValidationError('Статус с таким именем уже существует.')

            return name


class TypeForm(forms.ModelForm):
    """Форма типа транзакции"""
    class Meta:
        model = TypeTransaction
        fields = ['name']

    def clean_name(self):
        """Валидатор проверяющий наличие похожего типа"""
        name = self.cleaned_data.get('name')

        if name:
            cleaned_name = name.lower().strip()
            existing = TypeTransaction.objects.filter(name__iexact=cleaned_name)
            # Ищем категории с таким же именем (без учёта регистра) и тем же типом
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            # Проверка похожей записи
            if existing.exists():
                raise ValidationError('Тип транзакции с таким именем уже существует.')

            return name

class CategoryForm(forms.ModelForm):
    """Форма категории транзакции"""
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']  # ✅ Включаем 'transaction_type'

    def clean_name(self):
        """Валидатор проверяющий наличие похожей категории в рамках типа транзакции"""
        name = self.cleaned_data.get('name')
        transaction_type = self.cleaned_data.get('transaction_type')

        if name and transaction_type:
            cleaned_name = name.lower().strip()

            # Ищем категории с таким же именем (без учёта регистра) и тем же типом
            existing = Category.objects.filter(
                name__iexact=cleaned_name,
                transaction_type=transaction_type
            )

            # Если форма редактирует существующий объект
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            # Проверка похожей записи
            if existing.exists():
                raise ValidationError(
                    f'Категория с названием "{name}" уже существует для выбранного типа транзакции.'
                )

        return name


class SubcategoryForm(forms.ModelForm):  # Исправь имя класса
    """Форма подкатегории транзакции"""
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

    def clean_name(self):
        """Валидатор проверяющий наличие похожей подкатегории в рамках категории"""
        name = self.cleaned_data.get('name')
        category = self.cleaned_data.get('category')

        if name and category:
            cleaned_name = name.lower().strip()

            # Ищем подкатегории с таким же именем (без учёта регистра) и той же категорией
            existing = Subcategory.objects.filter(
                name__iexact=cleaned_name,
                category=category
            )

            # Если форма редактирует существующий объект
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            # Проверка похожей записи
            if existing.exists():
                raise ValidationError(
                    f'Подкатегория с названием "{name}" уже существует для выбранной категории.'
                )

        return name
