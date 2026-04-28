from django.contrib import admin
from .models import Workflow, WorkflowStep

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'workflow', 'role', 'step_order')
    list_filter = ('workflow',)
    ordering = ('workflow', 'step_order')