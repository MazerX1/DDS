from django.shortcuts import render, get_object_or_404, redirect
from .models import CashFlow, Status, Type, Category, SubCategory
from .forms import CashFlowForm, StatusForm, TypeForm, CategoryForm, SubCategoryForm

# -------------------
# Главная страница с фильтрацией
# -------------------
def index(request):
    cashflows = CashFlow.objects.all()
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    if date_from:
        cashflows = cashflows.filter(date__gte=date_from)
    if date_to:
        cashflows = cashflows.filter(date__lte=date_to)
    if status_id:
        cashflows = cashflows.filter(status_id=status_id)
    if type_id:
        cashflows = cashflows.filter(type_id=type_id)
    if category_id:
        cashflows = cashflows.filter(category_id=category_id)
    if subcategory_id:
        cashflows = cashflows.filter(subcategory_id=subcategory_id)

    context = {
        'cashflows': cashflows,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all()
    }
    return render(request, 'dds_app/index.html', context)

# -------------------
# CRUD записи ДДС
# -------------------
# Страница добавления записи
def cashflow_add(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            # Проверка бизнес-правил: категория принадлежит типу, подкатегория — категории
            type_selected = form.cleaned_data['type']
            category_selected = form.cleaned_data['category']
            subcategory_selected = form.cleaned_data['subcategory']

            if category_selected.type != type_selected:
                form.add_error('category', 'Категория не относится к выбранному типу.')
            elif subcategory_selected.category != category_selected:
                form.add_error('subcategory', 'Подкатегория не относится к выбранной категории.')
            else:
                form.save()
                return redirect('dds_app:index')
    else:
        form = CashFlowForm()

    # Передаем справочники и выбранные значения для шаблона
    context = {
        'form': form,
        'title': 'Добавить запись',
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'selected_type': request.POST.get('type') if request.method == 'POST' else '',
        'selected_category': request.POST.get('category') if request.method == 'POST' else '',
        'selected_subcategory': request.POST.get('subcategory') if request.method == 'POST' else '',
    }
    return render(request, 'dds_app/form.html', context)

def cashflow_edit(request, pk):
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cashflow)
        if form.is_valid():
            type_selected = form.cleaned_data['type']
            category_selected = form.cleaned_data['category']
            subcategory_selected = form.cleaned_data['subcategory']

            if category_selected.type != type_selected:
                form.add_error('category', 'Категория не относится к выбранному типу.')
            elif subcategory_selected.category != category_selected:
                form.add_error('subcategory', 'Подкатегория не относится к выбранной категории.')
            else:
                form.save()
                return redirect('dds_app:index')
    else:
        form = CashFlowForm(instance=cashflow)

    context = {
        'form': form,
        'title': 'Редактировать запись',
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'selected_type': cashflow.type.id if cashflow.type else '',
        'selected_category': cashflow.category.id if cashflow.category else '',
        'selected_subcategory': cashflow.subcategory.id if cashflow.subcategory else '',
    }
    return render(request, 'dds_app/form.html', context)
def cashflow_delete(request, pk):
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        cashflow.delete()
        return redirect('dds_app:index')
    return render(request, 'dds_app/delete_confirm.html', {'object': cashflow})

# -------------------
# Страница справочников
# -------------------
def catalog(request):
    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all()
    }
    return render(request, 'dds_app/catalog.html', context)

# -------------------
# CRUD для статусов
# -------------------
def status_add(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = StatusForm()
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Добавить статус'})

def status_edit(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = StatusForm(instance=obj)
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Редактировать статус'})

def status_delete(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('dds_app:catalog')
    return render(request, 'dds_app/delete_confirm.html', {'object': obj})

# -------------------
# CRUD для типов
# -------------------
def type_add(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = TypeForm()
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Добавить тип'})

def type_edit(request, pk):
    obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = TypeForm(instance=obj)
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Редактировать тип'})

def type_delete(request, pk):
    obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('dds_app:catalog')
    return render(request, 'dds_app/delete_confirm.html', {'object': obj})

# -------------------
# CRUD для категорий
# -------------------
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = CategoryForm()
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Добавить категорию'})

def category_edit(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = CategoryForm(instance=obj)
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Редактировать категорию'})

def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('dds_app:catalog')
    return render(request, 'dds_app/delete_confirm.html', {'object': obj})

# -------------------
# CRUD для подкатегорий
# -------------------
def subcategory_add(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = SubCategoryForm()
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Добавить подкатегорию'})

def subcategory_edit(request, pk):
    obj = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dds_app:catalog')
    else:
        form = SubCategoryForm(instance=obj)
    return render(request, 'dds_app/form.html', {'form': form, 'title': 'Редактировать подкатегорию'})

def subcategory_delete(request, pk):
    obj = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('dds_app:catalog')
    return render(request, 'dds_app/delete_confirm.html', {'object': obj})
