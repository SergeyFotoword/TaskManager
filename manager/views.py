# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import TaskSerializer
# from .models import Task
# from django.utils import timezone
# from django.db.models import Count
#
# '''
# Задание 1: Эндпоинт для создания задачи
# Создайте эндпоинт для создания новой задачи. Задача должна быть создана с полями title, description, status, и deadline.
# Шаги для выполнения:
# Определите сериализатор для модели Task.
# Создайте представление для создания задачи.
# Создайте маршрут для обращения к представлению.
# '''
#
# @api_view(['POST'])
# def create_task(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# '''
# Задание 2: Эндпоинты для получения списка задач и конкретной задачи по её ID
# Создайте два новых эндпоинта для:
# Получения списка задач
# Получения конкретной задачи по её уникальному ID
# Шаги для выполнения:
# Создайте представления для получения списка задач и конкретной задачи.
# Создайте маршруты для обращения к представлениям.
# '''
#
# @api_view(['GET'])
# def task_list(request):
#     tasks = Task.objects.all()
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# @api_view(['GET'])
# def task_detail(request, task_id):
#     try:
#         task = Task.objects.get(id=task_id)
#     except Task.DoesNotExist:
#         return Response(
#             {"error": "Task not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )
#
#     serializer = TaskSerializer(task)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# """
# Задание 3: Агрегирующий эндпоинт для статистики задач
# Создайте эндпоинт для получения статистики задач, таких как общее количество задач,
# количество задач по каждому статусу и количество просроченных задач.
# Шаги для выполнения:
# Определите представление для агрегирования данных о задачах.
# Создайте маршрут для обращения к представлению.
# """
#
# @api_view(['GET'])
# def task_stats(request):
#     now = timezone.now()
#
#     # total number of tasks
#     total_tasks = Task.objects.count()
#
#     # number of tasks for each status
#     status_counts = Task.objects.values('status').annotate(count=Count('status'))
#
#     # transform it into a convenient dictionary
#     status_data = {item['status']: item['count'] for item in status_counts}
#
#     # overdue tasks (deadline < now and status is not Done)
#     overdue_tasks = Task.objects.filter(deadline__lt=now).exclude(status="Done").count()
#
#     data = {
#         "total_tasks": total_tasks,
#         "status_stats": status_data,
#         "overdue_tasks": overdue_tasks
#     }
#
#     return Response(data, status=status.HTTP_200_OK)

# Задание 5: Создание классов представлений
# Создайте классы представлений для работы с подзадачами (SubTasks), включая создание, получение, обновление и удаление подзадач. Используйте классы представлений (APIView) для реализации этого функционала.
# Шаги для выполнения:
# Создайте классы представлений для создания и получения списка подзадач (SubTaskListCreateView).
# Создайте классы представлений для получения, обновления и удаления подзадач (SubTaskDetailUpdateDeleteView).
# Добавьте маршруты в файле urls.py, чтобы использовать эти классы.
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import(
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.decorators import action
from rest_framework import status
from .models import SubTask, Task, Category
from .serializers import (
    SubTaskSerializer,
    SubTaskCreateSerializer,
    TaskSerializer,
    CategorySerializer)
# from django.utils import timezone
# from rest_framework.decorators import api_view
from .pagination import SubTaskPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count

# class SubTaskListCreateView(APIView):
#
#     def get(self, request):
#         subtasks = SubTask.objects.all()
#         serializer = SubTaskSerializer(subtasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):

    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

WEEKDAYS_MAP = {
    "monday": 0, "понедельник": 0,
    "tuesday": 1, "вторник": 1,
    "wednesday": 2, "среда": 2,
    "thursday": 3, "четверг": 3,
    "friday": 4, "пятница": 4,
    "saturday": 5, "суббота": 5,
    "sunday": 6, "воскресенье": 6,
}
#
#
# @api_view(["GET"])
# def list_tasks_by_weekday(request):
#     weekday_param = request.query_params.get("weekday")
#
#     if not weekday_param:
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#
#     weekday_param = weekday_param.lower().strip()
#
#     if weekday_param not in WEEKDAYS_MAP:
#         return Response(
#             {"error": "Invalid day of the week"},
#             status=400
#         )
#
#     weekday_number = WEEKDAYS_MAP[weekday_param]
#
#     tasks = Task.objects.filter(deadline__week_day=weekday_number + 2)
#
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)

class TaskListByWeekdayView(GenericAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        weekday_param = self.request.query_params.get("weekday")

        if not weekday_param:
            return queryset

        weekday_param = weekday_param.lower().strip()

        if weekday_param not in WEEKDAYS_MAP:
            return None

        python_weekday = WEEKDAYS_MAP[weekday_param]

        # !!!!!Django использует другие week_day: Monday=2 → (python)Monday=0
        django_weekday = python_weekday + 2

        return queryset.filter(deadline__week_day=django_weekday)

    def get(self, request):
        queryset = self.get_queryset()

        if queryset is None:
            return Response(
                {"error": "Incorrect value for the weekday parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubTaskListView(GenericAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        return SubTask.objects.order_by("-created_at")

    def get(self, request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubTaskFilterView(GenericAPIView):
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by("-created_at")

        task_title = self.request.query_params.get("task_title")
        status_param = self.request.query_params.get("status")

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title.strip())

        if status_param:
            queryset = queryset.filter(status__iexact=status_param.strip())

        return queryset

    def get(self, request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # example:
    # /tasks/?status=Done
    # /tasks/?deadline=2025-01-30
    filterset_fields = ["status", "deadline"]

    # example:
    # /tasks/?search=presentation
    search_fields = ["title", "description"]

    # example:
    # /tasks/?ordering=created_at
    # /tasks/?ordering=-created_at
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "deadline"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class SubTaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    queryset = Category.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=False, methods=["get"])
    def count_tasks(self, request):
        categories = (
            self.get_queryset()
            .annotate(tasks_count=Count("tasks"))
        )

        return Response([
            {
                "category_id": category.id,
                "name": category.name,
                "tasks_count": category.tasks_count,
            }
            for category in categories
        ])