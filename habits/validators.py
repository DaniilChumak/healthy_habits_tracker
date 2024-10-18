from datetime import timedelta

from rest_framework import serializers


class DurationValidator:
    """Время выполнения должно быть не больше 120 секунд."""

    def __call__(self, value):
        if value:
            if value > timedelta(minutes=2):
                raise serializers.ValidationError(
                    "Время на выполнение не должно превышать 120 секунд"
                )


class PeriodValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""

    def __call__(self, value):
        if value:
            if not 1 <= value <= 7:
                raise serializers.ValidationError(
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"
                )


class PleasantHabitValidator:
    """У приятной привычки не может быть
    вознаграждения или связанной привычки"""

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        if value.get(self.field1) and (
            value.get(self.field2) or value.get(self.field3)
        ):
            raise serializers.ValidationError(
                "У приятной привычки не может быть"
                "вознаграждения или связанной привычки"
            )


class PleasantHabitOrRewardValidator:
    """Исключение одновременного выбора
    связанной привычки и указания вознаграждения"""

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        if value.get(self.field1) and value.get(self.field2):
            raise serializers.ValidationError(
                "У полезной привычки не может быть вознаграждения"
                "и связанной привычки одновременно"
            )


class RelatedHabitValidator:
    """В связанные привычки могут попадать
    только привычки с признаком приятной привычки"""

    def __init__(self, field1):
        self.field1 = field1

    def __call__(self, value):
        if value.get(self.field1):
            if not value.get(self.field1).is_pleasant:
                raise serializers.ValidationError(
                    "В связанные привычки могут попадать"
                    "только привычки с признаком приятной привычки"
                )