# models.py
from decimal import Decimal
from typing import Dict, Any

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone  # ДОБАВИТЬ!
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class PayoutStatus(models.TextChoices):
    PENDING = "pending", _("В ожидании")
    PROCESSING = "processing", _("В обработке")
    COMPLETED = "completed", _("Выполнена")
    FAILED = "failed", _("Не удалась")
    CANCELLED = "cancelled", _("Отменена")


class Currency(models.TextChoices):
    RUB = "RUB", _("Российский рубль")
    USD = "USD", _("Доллар США")
    EUR = "EUR", _("Евро")
    GBP = "GBP", _("Фунт стерлингов")


class Payout(BaseModel):
    amount: Decimal = models.DecimalField(
        _("Сумма"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    currency = models.CharField(
        _("Валюта"),
        max_length=3,
        choices=Currency.choices,
        default=Currency.RUB,
    )

    recipient_details: Dict[str, Any] = models.JSONField(
        _("Реквизиты получателя"),
        help_text=_("Данные получателя в формате JSON"),
    )

    status = models.CharField(
        _("Статус"),
        max_length=20,
        choices=PayoutStatus.choices,
        default=PayoutStatus.PENDING,
        db_index=True,
    )

    description = models.TextField(
        _("Описание"),
        blank=True,
        null=True,
    )

    processed_at = models.DateTimeField(
        _("Время обработки"),
        blank=True,
        null=True,
    )

    completed_at = models.DateTimeField(
        _("Время завершения"),
        blank=True,
        null=True,
    )

    def mark_as_processing(self) -> None:
        self.status = PayoutStatus.PROCESSING
        self.processed_at = timezone.now()  # Добавить это!
        self.save(update_fields=['status'])

    def mark_as_completed(self):
        self.status = PayoutStatus.COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

    def mark_as_failed(self):
        self.status = PayoutStatus.FAILED
        self.save(update_fields=['status'])

    def can_be_deleted(self) -> bool:
        return self.status in [PayoutStatus.PENDING, PayoutStatus.FAILED]

    def get_recipient_name(self) -> str:
        return self.recipient_details.get('account_holder', 'Unknown')

    @property
    def display_status(self):
        return dict(PayoutStatus.choices).get(self.status, 'Unknown')

    @property
    def display_currency(self):
        return dict(Currency.choices).get(self.currency, 'Unknown')

    class Meta:
        verbose_name = _("Выплата")
        verbose_name_plural = _("Выплаты")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payout #{self.id} - {self.amount} {self.currency}"