from django.contrib import admin
from .models import Category, Task, SubTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "deadline", "created_at")
    list_filter = ("status", "created_date")
    search_fields = ("title", "description")
    date_hierarchy = "created_date"
    filter_horizontal = ("categories",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "deadline", "created_at")
    list_filter = ("status", "task")
    search_fields = ("title", "description")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
