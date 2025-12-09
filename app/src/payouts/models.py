# models.py
from decimal import Decimal
from typing import Any, Dict

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone  # ДОБАВИТЬ!
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
import logging
import os

logger = logging.getLogger("payout-status")
if not logger.handlers:
    log_dir = "/app/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler("/app/logs/status.log")
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)


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
        logger.info(f"Начинаем обработку выплаты #{self.id}")
        self.status = PayoutStatus.PROCESSING
        self.processed_at = timezone.now()
        self.save(update_fields=["status"])
        logger.info(f"Выплата #{self.id} в обработке")

    def mark_as_completed(self):
        logger.info(f"Завершаем выплату #{self.id}")
        self.status = PayoutStatus.COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at"])
        logger.info(f"Выплата #{self.id} завершена!")

    def mark_as_failed(self):
        self.status = PayoutStatus.FAILED
        self.save(update_fields=["status"])

    def can_be_deleted(self) -> bool:
        return self.status in [PayoutStatus.PENDING, PayoutStatus.FAILED]

    def get_recipient_name(self) -> str:
        return self.recipient_details.get("account_holder", "Unknown")

    @property
    def display_status(self):
        return dict(PayoutStatus.choices).get(self.status, "Unknown")

    @property
    def display_currency(self):
        return dict(Currency.choices).get(self.currency, "Unknown")

    class Meta:
        verbose_name = _("Выплата")
        verbose_name_plural = _("Выплаты")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payout #{self.id} - {self.amount} {self.currency}"
