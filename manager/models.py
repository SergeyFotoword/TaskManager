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
'''
Добавить метод str, который возвращает название задачи.
Добавить класс Meta с настройками:
Имя таблицы в базе данных: 'task_manager_task'.
Сортировка по убыванию даты создания.
Человекочитаемое имя модели: 'Task'.
Уникальность по полю 'title'.
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
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_task_title')
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

'''
Добавить метод str, который возвращает название подзадачи.
Добавить класс Meta с настройками:
Имя таблицы в базе данных: 'task_manager_subtask'.
Сортировка по убыванию даты создания.
Человекочитаемое имя модели: 'SubTask'.
Уникальность по полю 'title'.
'''

class SubTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(max_length=15, choices=list_status, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]

'''
Модель Category:
Описание: Категория выполнения.
Поля:
name: Название категории.
'''

'''
Добавить метод str, который возвращает название категории.
Добавить класс Meta с настройками:
Имя таблицы в базе данных: 'task_manager_category'.
Человекочитаемое имя модели: 'Category'.
Уникальность по полю 'name'.
'''

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]
