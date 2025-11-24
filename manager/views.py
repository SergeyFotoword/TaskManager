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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SubTask
from .serializers import SubTaskSerializer, SubTaskCreateSerializer


class SubTaskListCreateView(APIView):

    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
