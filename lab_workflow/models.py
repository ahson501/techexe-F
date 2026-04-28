from django.db import models
from django.contrib.auth.models import User

# =========================
# WORKFLOW TEMPLATE
# =========================

class Workflow(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="steps")
    role = models.CharField(max_length=50)  # e.g. supervisor, manager, director
    step_order = models.PositiveIntegerField()

    class Meta:
        ordering = ['step_order']
        unique_together = ('workflow', 'step_order')

    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order} ({self.role})"


# =========================
# MAIN UPLC REQUEST
# =========================

class UPLCRequest(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uplc_requests")
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="supervised_requests")
    workflow = models.ForeignKey(Workflow, on_delete=models.SET_NULL, null=True, blank=True)

    # Basic Info
    sample_code = models.CharField(max_length=100)
    intercom = models.CharField(max_length=50, blank=True)

    # Form Fields
    sample_type = models.TextField()
    solubility = models.CharField(max_length=200)
    wavelength = models.FloatField()
    flow_rate = models.FloatField()
    solvent_a = models.CharField(max_length=100, blank=True)
    solvent_b = models.CharField(max_length=100, blank=True)
    column = models.CharField(max_length=200, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"UPLC: {self.sample_code} ({self.status})"


# =========================
# MAIN NMR REQUEST
# =========================

class NMRRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)
    supervisor = models.CharField(max_length=255) # Text field as per form
    thesis_title = models.CharField(max_length=500, blank=True, null=True)
    date_submitted = models.DateField(auto_now_add=True)
    lab_no = models.CharField(max_length=50, blank=True, null=True)
    extension_no = models.CharField(max_length=50, blank=True, null=True)

    # Sample Details
    sample_code = models.CharField(max_length=100)
    solvent = models.CharField(max_length=100, blank=True, null=True)
    solubility = models.CharField(max_length=100, blank=True, null=True)
    molecular_weight = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    concentration = models.CharField(max_length=100, blank=True, null=True)
    
    # Optional NMR Status Fields (The ones that caused the error)
    status_h_nmr = models.CharField(max_length=255, verbose_name="Status of 1H NMR", blank=True, null=True)
    status_c_nmr = models.CharField(max_length=255, verbose_name="Status of 13C NMR", blank=True, null=True)

    # Techniques (Checkboxes)
    # 2D-Homonuclear
    cosy = models.BooleanField(default=False)
    noesy = models.BooleanField(default=False)
    roesy = models.BooleanField(default=False)
    j_resolved = models.BooleanField(default=False)
    tocsy = models.BooleanField(default=False)
    dosy = models.BooleanField(default=False)
    dipsi = models.BooleanField(default=False)

    # 2D-Heteronuclear
    hsqc = models.BooleanField(default=False)
    hmbc = models.BooleanField(default=False)
    x_j_resolved = models.BooleanField(default=False)
    hmqc_cosy = models.BooleanField(default=False)

    # Concatenated
    dept_hqqc = models.BooleanField(default=False)
    hsqc_tocsy = models.BooleanField(default=False)
    hsqc_noesy = models.BooleanField(default=False)

    # Requirements
    data_format = models.CharField(
        max_length=20, 
        choices=[('Hard Copy', 'Hard Copy'), ('Soft Copy', 'Soft Copy')],
        blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"NMR: {self.sample_code} ({self.status})"


# =========================
# APPROVAL INSTANCE
# =========================

class Approval(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    uplc_request = models.ForeignKey(UPLCRequest, on_delete=models.CASCADE, related_name="approvals", null=True, blank=True)
    nmr_request = models.ForeignKey(NMRRequest, on_delete=models.CASCADE, related_name="approvals", null=True, blank=True)
    step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approvals")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True)
    action_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['step__step_order']
        # Removed unique_together because it only allowed UPLC requests

    def __str__(self):
        if self.uplc_request:
            sample = self.uplc_request.sample_code
        elif self.nmr_request:
            sample = self.nmr_request.sample_code
        else:
            sample = "Unknown"
        return f"{sample} - {self.action}"
# =========================
# AUDIT LOG
# =========================

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('updated', 'Updated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uplc_request = models.ForeignKey(UPLCRequest, on_delete=models.CASCADE, related_name="logs", null=True, blank=True)
    nmr_request = models.ForeignKey(NMRRequest, on_delete=models.CASCADE, related_name="logs", null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        # Improved __str__ to handle both types of requests
        sample = self.request.sample_code if self.request else self.nmr_request.sample_code if self.nmr_request else "Unknown"
        return f"{sample} - {self.action}"