from django import forms
from .models import CashFlow, Status, Type, Category, SubCategory


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select', 'id': 'type-select'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'category-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select', 'id': 'subcategory-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Валидация обязательных полей
        for field in ['amount', 'type', 'category', 'subcategory']:
            if not cleaned_data.get(field):
                self.add_error(field, 'Это поле обязательно к заполнению.')

        # Бизнес-правила: подкатегория соответствует категории
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        if subcategory and subcategory.category != category:
            self.add_error('subcategory', 'Подкатегория не соответствует выбранной категории.')

        # Бизнес-правила: категория соответствует типу
        type_ = cleaned_data.get('type')
        if category and category.type != type_:
            self.add_error('category', 'Категория не соответствует выбранному типу.')

        return cleaned_data


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
