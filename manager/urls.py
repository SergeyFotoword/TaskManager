from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    # list_tasks_by_weekday,
    TaskListByWeekdayView,
    SubTaskListView,
    SubTaskFilterView,
    TaskListCreateView,
    TaskDetailView,
    SubTaskDetailView,
)

router = DefaultRouter()
router.register(
    r"categories",
    CategoryViewSet,
    basename="category"
)

urlpatterns = [
    path("", include(router.urls)),
    path("subtasks/", SubTaskListCreateView.as_view()),
    # path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view()),
    # path("tasks/", list_tasks_by_weekday),
    path("tasks/weekday/", TaskListByWeekdayView.as_view()),
    # path("subtasks", SubTaskListView.as_view()),
    path("subtasks/filter", SubTaskFilterView.as_view()),
    path("tasks/", TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
    path("subtasks/<int:pk>/", SubTaskDetailView.as_view()),
]
