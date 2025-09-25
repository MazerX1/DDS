from django.urls import path
from . import views

app_name = 'dds_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.cashflow_add, name='add'),
    path('edit/<int:pk>/', views.cashflow_edit, name='edit'),
    path('delete/<int:pk>/', views.cashflow_delete, name='delete'),
    path('catalog/', views.catalog, name='catalog'),

    # Статусы
    path('status/add/', views.status_add, name='status_add'),
    path('status/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('status/delete/<int:pk>/', views.status_delete, name='status_delete'),

    # Типы
    path('type/add/', views.type_add, name='type_add'),
    path('type/edit/<int:pk>/', views.type_edit, name='type_edit'),
    path('type/delete/<int:pk>/', views.type_delete, name='type_delete'),

    # Категории
    path('category/add/', views.category_add, name='category_add'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Подкатегории
    path('subcategory/add/', views.subcategory_add, name='subcategory_add'),
    path('subcategory/edit/<int:pk>/', views.subcategory_edit, name='subcategory_edit'),
    path('subcategory/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),
]
