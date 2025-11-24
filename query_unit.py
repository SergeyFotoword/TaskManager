from datetime import date, timedelta
from manager.models import Task, SubTask
from django.utils import timezone

"""
Task:
title: "Prepare presentation".
description: "Prepare materials and slides for the presentation".
status: "New".
deadline: Today's date + 3 days.
"""

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3)
)

# task = Task.objects.get(id=4)
# task.delete()

'''
SubTasks для "Prepare presentation":
title: "Gather information".
description: "Find necessary information for the presentation".
status: "New".
deadline: Today's date + 2 days.
'''
subtask1 = SubTask.objects.create(
    task=task,
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=2)
)


subtask2 = SubTask.objects.create(
    task=task,
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=timezone.now() + timedelta(days=1)
)

'''
SubTasks для "Prepare presentation":
title: "Create slides".
description: "Create presentation slides".
status: "New".
deadline: Today's date + 1 day.
'''

subtask2 = SubTask.objects.create(
    task=task,
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=timezone.now() + timedelta(days=1)
)

'''
Tasks со статусом "New":
Вывести все задачи, у которых статус "New".
'''

new_tasks = Task.objects.filter(status="New")
for nt in new_tasks:
    print(f"{nt.title} - {nt.status} - {nt.deadline}")


'''
SubTasks с просроченным статусом "Done":
Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
'''

expired_done_subtasks = SubTask.objects.filter(
    status="Done",
    deadline__lt=timezone.now()
)
for eds in expired_done_subtasks:
    print(f"{eds.title} - {eds.status} - {eds.deadline}")

# Таких задач, к сожалению, нет, а создавать -- облом, очень много работы.

# Измените статус "Prepare presentation" на "In progress".

task = Task.objects.get(title="Prepare presentation")
task.status = "In progress"
task.save()

# Измените срок выполнения для "Gather information" на два дня назад.
subtask1 = SubTask.objects.get(title="Gather information")
subtask1.deadline = timezone.now() - timedelta(days=2)
subtask1.save()

# Если стартуем день с нуля часов:
subtask1 = SubTask.objects.get(title="Gather information")
dt = timezone.localtime() - timedelta(days=2)
subtask1.deadline = dt.replace(hour=0, minute=0, second=0, microsecond=0)
subtask1.save()

# Измените описание для "Create slides" на "Create and format presentation slides".
subtask2 = SubTask.objects.get(title="Create slides")
subtask2.description = "Create and format presentation slides"
subtask2.save()

# Удалите задачу "Prepare presentation" и все ее подзадачи.
#on_delete=models.CASCADE, значит:

deleted_count, details = Task.objects.filter(title="Prepare presentation").delete()
print(f"Удалено записей: {deleted_count}. Детали таковы: {details}")

