from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# ==========================================================
# CHOICES
# ==========================================================

class AssignmentType(models.TextChoices):
    GROUP = "GROUP", "Specific Group"
    SUPERVISOR = "SUPERVISOR", "Applicant Supervisor"
    HOD = "HOD", "Head of Department"
    DIRECTOR = "DIRECTOR", "Director"
    USER = "USER", "Specific User"


class WorkflowStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    RETURNED = "RETURNED", "Returned"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"
    COMPLETED = "COMPLETED", "Completed"


class TaskStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    RETURNED = "RETURNED", "Returned"
    SKIPPED = "SKIPPED", "Skipped"


class ActionType(models.TextChoices):
    SUBMIT = "SUBMIT", "Submitted"
    APPROVE = "APPROVE", "Approved"
    REJECT = "REJECT", "Rejected"
    RETURN = "RETURN", "Returned"
    CANCEL = "CANCEL", "Cancelled"


# ==========================================================
# WORKFLOW CONFIGURATION
# ==========================================================

class WorkflowConfig(models.Model):
    """
    Defines workflow for a specific form/model.
    Example:
        LeaveApplication
        ITComplaint
        UPLCRequest
    """

    name = models.CharField(max_length=100, unique=True)

    content_type = models.OneToOneField(
        ContentType,
        on_delete=models.CASCADE
    )

    description = models.TextField(blank=True)

    version = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (v{self.version})"


class WorkflowStep(models.Model):
    """
    Approval chain definition.
    """

    workflow = models.ForeignKey(
        WorkflowConfig,
        on_delete=models.CASCADE,
        related_name="steps"
    )

    step_number = models.PositiveIntegerField()

    step_name = models.CharField(max_length=150)

    assignment_type = models.CharField(
        max_length=20,
        choices=AssignmentType.choices,
        default=AssignmentType.GROUP
    )

    assigned_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    assigned_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    can_return = models.BooleanField(default=True)

    can_delegate = models.BooleanField(default=False)

    is_optional = models.BooleanField(default=False)

    timeout_days = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["step_number"]
        unique_together = ("workflow", "step_number")

    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_number}: {self.step_name}"


# ==========================================================
# ACTIVE WORKFLOW INSTANCE
# ==========================================================

class WorkflowInstance(models.Model):
    """
    One workflow attached to one submitted form.
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.PositiveIntegerField()

    form_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    workflow = models.ForeignKey(
        WorkflowConfig,
        on_delete=models.PROTECT
    )

    current_step = models.ForeignKey(
        WorkflowStep,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    submitted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="submitted_workflows"
    )

    current_actor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_workflows"
    )

    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.SUBMITTED
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.workflow.name} #{self.pk}"


# ==========================================================
# CURRENT APPROVAL TASK
# ==========================================================

class ApprovalTask(models.Model):
    """
    Pending work assigned to approver.
    """

    workflow_instance = models.ForeignKey(
        WorkflowInstance,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    step = models.ForeignKey(
        WorkflowStep,
        on_delete=models.CASCADE
    )

    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    assigned_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )

    assigned_on = models.DateTimeField(auto_now_add=True)

    completed_on = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["assigned_on"]

    def __str__(self):
        return f"{self.assigned_to} - {self.step.step_name}"


# ==========================================================
# COMPLETE AUDIT LOG
# ==========================================================

class WorkflowLog(models.Model):
    """
    Immutable audit trail.
    """

    workflow_instance = models.ForeignKey(
        WorkflowInstance,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    step = models.ForeignKey(
        WorkflowStep,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    actor = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    action = models.CharField(
        max_length=20,
        choices=ActionType.choices
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.actor} - {self.action}"
