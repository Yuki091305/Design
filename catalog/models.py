from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from uuid import uuid4


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Название категории")

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    REQUEST_STATUS = (
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    )

    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)

    # План помещения от пользователя
    attachment = models.FileField(
        upload_to='plans/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])]
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='new')

    # Для админа
    admin_comment = models.TextField(blank=True)
    design_image = models.FileField(upload_to='designs/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

