from django.contrib import admin
from .models import WorkflowConfig, WorkflowStep, WorkflowInstance, ApprovalTask, WorkflowLog

class WorkflowStepInline(admin.TabularInline):
    """ Allows you to define steps (1, 2, 3...) right inside the Workflow Config page """
    model = WorkflowStep
    extra = 1
    ordering = ['step_number']

@admin.register(WorkflowConfig)
class WorkflowConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'version', 'is_active', 'created_at')
    list_filter = ('is_active', 'version')
    search_fields = ('name',)
    inlines = [WorkflowStepInline]

@admin.register(WorkflowInstance)
class WorkflowInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'workflow', 'content_type', 'object_id', 'status', 'submitted_by', 'current_actor', 'submitted_at')
    list_filter = ('status', 'workflow', 'submitted_at')
    search_fields = ('submitted_by__username', 'current_actor__username', 'object_id')
    readonly_fields = ('submitted_at', 'completed_at')

@admin.register(ApprovalTask)
class ApprovalTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'workflow_instance', 'step', 'assigned_to', 'status', 'assigned_on', 'completed_on')
    list_filter = ('status', 'assigned_on')
    search_fields = ('assigned_to__username', 'workflow_instance__id')

@admin.register(WorkflowLog)
class WorkflowLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'workflow_instance', 'step', 'actor', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('actor__username', 'workflow_instance__id', 'remarks')
    
    # Make logs read-only in admin so nobody can manipulate history data
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
