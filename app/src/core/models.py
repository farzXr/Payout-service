from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Создано"),
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        _("Обновлено"),
        auto_now=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
