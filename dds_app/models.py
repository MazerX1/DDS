import datetime

from django.db import models

class Status(models.Model):
    name = models.CharField("Название статуса", max_length=50)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField("Тип", max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField("Категория", max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.name} ({self.type.name})"

class SubCategory(models.Model):
    name = models.CharField("Подкатегория", max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class CashFlow(models.Model):
    date = models.DateField(default=datetime.date.today)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    amount = models.DecimalField("Сумма", max_digits=12, decimal_places=2)
    comment = models.TextField("Комментарий", blank=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.date:
            # Если запись новая и дата не указана, ставим сегодня
            self.date = models.DateField.auto_now_add
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.amount} р."

    def clean(self):
        """Проверка бизнес-логики: категории и подкатегории соответствуют типу."""
        from django.core.exceptions import ValidationError
        if self.subcategory.category != self.category:
            raise ValidationError("Подкатегория не соответствует выбранной категории")
        if self.category.type != self.type:
            raise ValidationError("Категория не соответствует выбранному типу")