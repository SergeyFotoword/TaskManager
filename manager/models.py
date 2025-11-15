from django.db import models

'''
Модель Task:
Описание: Задача для выполнения.
Поля:
title: Название задачи. Уникально для даты.
description: Описание задачи.
categories: Категории задачи. Многие ко многим.
status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
deadline: Дата и время дедлайн.
created_at: Дата и время создания. Автоматическое заполнение.
'''

list_status = [
    ('new', 'Новая'),
    ('in_progress', 'В процессе'),
    ('pending', 'Приостановлена'),
    ('blocked', 'Заблокирована'),
    ('done', 'Завершена'),
]

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField('Category', related_name='tasks', blank=True)
    status = models.CharField(max_length=15, choices=list_status, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "created_date"],
                name="unique_title_per_day",
            )
        ]

'''
Модель SubTask:
Описание: Отдельная часть основной задачи (Task).
Поля:
title: Название подзадачи.
description: Описание подзадачи.
task: Основная задача. Один ко многим.
status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
deadline: Дата и время дедлайн.
created_at: Дата и время создания. Автоматическое заполнение.
'''

class SubTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(max_length=15, choices=list_status, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

'''
Модель Category:
Описание: Категория выполнения.
Поля:
name: Название категории.
'''

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name