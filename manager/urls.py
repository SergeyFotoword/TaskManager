from django.urls import path
from .views import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path("subtasks/", SubTaskListCreateView.as_view()),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view()),
]