from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import MyPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


# Create your views here.
class HabitListAPIView(generics.ListAPIView):
    """Habit list endpoint"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination
    #
    # def get(self, request):
    #     queryset = Habit.objects.all()
    #     paginated_queryset = self.paginate_queryset(queryset)
    #     serializer = HabitSerializer(paginated_queryset, many=True)
    #     return self.get_paginated_response(serializer.data)


class MyHabitListAPIView(HabitListAPIView):
    """User's habit list endpoint"""

    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            queryset = Habit.objects.filter(owner=user)
        else:
            queryset = Habit.objects.all()
        return queryset


class HabitCreateAPIView(generics.CreateAPIView):
    """Habit create endpoint"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.users.add(self.request.user)
        habit.save()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Habit retrieve endpoint"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Habit update endpoint"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Habit delete endpoint"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
