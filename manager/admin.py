from django.contrib import admin
from .models import Category, Task, SubTask

class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "short_title", "status", "deadline", "created_at")
    list_filter = ("status", "created_date")
    search_fields = ("title", "description")
    date_hierarchy = "created_date"
    filter_horizontal = ("categories",)
    inlines = [SubTaskInline]

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "deadline", "created_at")
    list_filter = ("status", "task", "deadline")
    search_fields = ("title", "description")
    actions = ["mark_as_done"]

    def mark_as_done(self, request, queryset):
        """Change the selected subtasks to Done status"""
        updated = queryset.update(status="Done")
        self.message_user(request, f"{updated} subtasks have been moved to Done status.")

    mark_as_done.short_description = "Mark selected as Done"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

