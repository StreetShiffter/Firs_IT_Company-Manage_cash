from django import forms
from django.core.exceptions import ValidationError
from manage_cash.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status',
                  'type',
                  'category',
                  'subcategory',
                  'amount',
                  'comment',
                  'date'
                  ]

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Статус транзакции'})

        self.fields['type'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Тип транзакции'})

        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Категория транзакции (зависит от типа транзакции)'})

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
