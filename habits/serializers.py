
from rest_framework import serializers

from habits.models import Habit
from habits.validators import (DurationValidator, PeriodValidator,
                               PleasantHabitOrRewardValidator,
                               PleasantHabitValidator, RelatedHabitValidator)


class HabitSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(validators=[DurationValidator()])
    period = serializers.IntegerField(validators=[PeriodValidator()])

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            PleasantHabitValidator(
                field1="is_pleasant", field2="reward", field3="related_habit"
            ),
            PleasantHabitOrRewardValidator(
                field1="reward", field2="related_habit"
            ),
            RelatedHabitValidator(field1="related_habit"),
        ]
