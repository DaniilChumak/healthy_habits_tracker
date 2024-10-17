from datetime import datetime, timedelta

import pytz
from django.db import models

from config import settings
from config.settings import AUTH_USER_MODEL
from users.models import NULLABLE, User

zone = pytz.timezone(settings.TIME_ZONE)
current_datetime = datetime.now(zone)


# Create your models here.
class Habit(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
        related_name="owner",
    )
    place = models.CharField(
        max_length=100,
        verbose_name="Место"
    )
    time = models.DateTimeField(
        default=current_datetime,
        verbose_name="Время (YYYY-MM-DD hh-mm)"
    )
    action = models.CharField(
        max_length=100,
        verbose_name="Действие"
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Связанная приятная привычка",
    )
    period = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дней)"
    )
    reward = models.CharField(
        max_length=100,
        **NULLABLE,
        verbose_name="Вознаграждение"
    )
    duration = models.DurationField(
        default=timedelta(minutes=2),
        verbose_name="Время на выполение (секунд)"
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="Признак публичности"
    )
    users = models.ManyToManyField(
        User,
        verbose_name="Пользователи",
        related_name="users",
        **NULLABLE
    )

    def __str__(self):
        return f"{self.action} в {self.time} {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("action",)
