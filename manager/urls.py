from django.urls import path
from .views import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    # list_tasks_by_weekday,
    TaskListByWeekdayView,
    SubTaskListView,
    SubTaskFilterView,
)

urlpatterns = [
    path("subtasks/", SubTaskListCreateView.as_view()),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view()),
    # path("tasks/", list_tasks_by_weekday),
    path("tasks/weekday", TaskListByWeekdayView.as_view()),
    path("subtasks", SubTaskListView.as_view()),
    path("subtasks/filter", SubTaskFilterView.as_view()),
]