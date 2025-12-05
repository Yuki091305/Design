from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid
from django.conf import settings
from datetime import date
from django.core.validators import MinLengthValidator


class Category(models.Model):
    """
    Модель, представляющая категорию заявки (например, 3D-дизайн, Эскиз).
    Управляется администратором.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Введите название категории (например, 3D-дизайн, Эскиз)"
    )

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name

    def get_absolute_url(self):
        """Возвращает URL для доступа к конкретному экземпляру категории."""
        # Вам нужно будет определить URL pattern с именем 'category-detail'
        return reverse('category-detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        constraints = [
            # Обеспечивает уникальность названия категории без учета регистра
            UniqueConstraint(
                Lower('name'),
                name='category_name_case_insensitive_unique',
                violation_error_message="Категория с таким названием уже существует (без учета регистра)"
            ),
        ]


class DesignRequest(models.Model):
    REQUEST_STATUS = (
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, help_text="Название проекта")
    description = models.TextField(max_length=1000, help_text="Опишите, что вы хотите")

    # Вот это — главное, что просили: загрузка плана
    attachment = models.FileField(
        upload_to='design_uploads/',
        blank=True,
        null=True,
        help_text="Загрузите план помещения (фото, PDF и т.п.)"
    )

    design_image = models.ImageField(
        upload_to='design_results/',
        blank=True,
        null=True,
        help_text="Готовый дизайн (только для статуса 'Выполнено')"
    )

    admin_comment = models.TextField(
        blank=True,
        null=True,
        help_text="Комментарий от дизайнера"
    )

    category = models.ForeignKey('Category', on_delete=models.RESTRICT, null=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Заявка на дизайн"
        verbose_name_plural = "Заявки на дизайн"

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'


    class Meta:
        ordering = ['-created_at']  # Сортировка по дате создания (новые сверху)
        verbose_name = "Заявка на дизайн"
        verbose_name_plural = "Заявки на дизайн"

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'

    def get_absolute_url(self):
        return reverse('request-detail', args=[str(self.id)]) # Нужен URL request-detail