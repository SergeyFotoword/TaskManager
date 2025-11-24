# from rest_framework import serializers
# from .models import Task
#
#
# """
# Задание 1: Эндпоинт для создания задачи
# Создайте эндпоинт для создания новой задачи. Задача должна быть создана с полями title, description, status, и deadline.
# Шаги для выполнения:
# Определите сериализатор для модели Task.
# Создайте представление для создания задачи.
# Создайте маршрут для обращения к представлению.
# """
#
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ["title", "description", "status", "deadline"]

# Homework 13

'''
Задание 1: Переопределение полей сериализатора
Создайте SubTaskCreateSerializer, в котором поле created_at будет доступно только для чтения (read_only).
Шаги для выполнения:
Определите SubTaskCreateSerializer в файле serializers.py.
Переопределите поле created_at как read_only.
'''


from rest_framework import serializers
from .models import SubTask, Category, Task
from django.utils import timezone


class SubTaskCreateSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            "id"
            "title",
            "description",
            "status",
            "deadline",
            "task",
            "created_at",
        ]
# or
#
# class SubTaskCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubTask
#         fields = '__all__'
#         read_only_fields = ['created_at', 'id']


'''
Задание 2: Переопределение методов create и update
Создайте сериализатор для категории CategoryCreateSerializer, переопределив методы create и update для проверки уникальности названия категории. Если категория с таким названием уже существует, возвращайте ошибку валидации.
Шаги для выполнения:
Определите CategoryCreateSerializer в файле serializers.py.
Переопределите метод create для проверки уникальности названия категории.
Переопределите метод update для аналогичной проверки при обновлении.
'''

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "created_at"]

    def validate_title(self, value):

        category_id = self.instance.id if self.instance else None

        # Checking the existence of a category with the same name
        # we exclude the category itself, not the duplicate
        qs = Category.objects.filter(title__iexact=value)
        if category_id:
            qs = qs.exclude(id=category_id)

        if qs.exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value

    def create(self, validated_data):
        title = validated_data.get("title")
        self.validate_title(title)

        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):

        title = validated_data.get("title", instance.title)
        self.validate_title(title)

        instance.title = title
        instance.save()
        return instance

'''
Задание 3: Использование вложенных сериализаторов
Создайте сериализатор для TaskDetailSerializer, который включает вложенный сериализатор для полного отображения связанных подзадач (SubTask). Сериализатор должен показывать все подзадачи, связанные с данной задачей.
Шаги для выполнения:
Определите TaskDetailSerializer в файле serializers.py.
Вложите SubTaskSerializer внутрь TaskDetailSerializer.
'''

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "subtasks",
        ]

'''
Задание 4: Валидация данных в сериализаторах
Создайте TaskCreateSerializer и добавьте валидацию для поля deadline, чтобы дата не могла быть в прошлом. Если дата в прошлом, возвращайте ошибку валидации.
Шаги для выполнения:
Определите TaskCreateSerializer в файле serializers.py.
Переопределите метод validate_deadline для проверки даты.
'''

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_deadline(self, value):

        now = timezone.now()

        if value < now:
            raise serializers.ValidationError(
                "Deadline can't be in the past."
            )

        return value
