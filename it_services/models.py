from django.db import models
from django.contrib.auth.models import User

class ICCBSBaseForm(models.Model):
    """ Shared structural header found on all ICCBS institutional sheets """
    UNIT_CHOICES = [
        ('HEJ', 'H.E.J.'), 
        ('PCMD', 'PCMD'), 
        ('LEJ', 'L.E.J.'), 
        ('TWC', 'TWC'), 
        ('OTHERS', 'OTHERS')
    ]
    
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    doc_no = models.CharField(max_length=50, editable=False)
    revision_no = models.CharField(max_length=5, editable=False)
    revision_date = models.DateField(editable=False)
    
    # CRITICAL: This links directly to your engine's routing rules
    submitted_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(class)s_submissions")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ITComplaint(ICCBSBaseForm):
    """ Matches Document No: ICCBS/QF/QSP-IT/ITCF """
    USER_TYPE_CHOICES = [('FACULTY', 'Faculty'), ('STUDENT', 'Student'), ('STAFF', 'Staff')]
    NATURE_CHOICES = [('HARDWARE', 'Hardware'), ('SOFTWARE', 'Software'), ('NETWORK', 'Network')]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    complainer_name = models.CharField(max_length=150)
    supervisor_name = models.CharField(max_length=150)
    lab_dept = models.CharField(max_length=100, verbose_name="Lab / Department")
    intercom_no = models.CharField(max_length=30)
    problem_description = models.TextField()
    
    # Handled by IT Engineers during step updates
    nature_of_problem = models.CharField(max_length=15, choices=NATURE_CHOICES, blank=True, null=True)
    it_staff_remarks = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(null=True, blank=True)
    service_satisfaction = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"IT Complaint by {self.complainer_name} ({self.created_on.date()})"


class EmailAccountCreation(ICCBSBaseForm):
    """ Matches Document No: ICCBS/QF/QSP-L.T-05 """
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    lab_no = models.CharField(max_length=30)
    intercom_no = models.CharField(max_length=30)
    contact_no = models.CharField(max_length=30)
    attendance_id = models.CharField(max_length=50)
    requested_email = models.EmailField(help_text="e.g. username@iccs.edu")
    alternate_email = models.EmailField()
    
    # Fulfilled by IT Staff on final step execution
    assigned_email = models.EmailField(blank=True, null=True)
    temporary_password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"Email Request: {self.first_name} {self.last_name}"


class ZoomLinkRegistration(ICCBSBaseForm):
    """ Dynamic tracking for Zoom Webinar/Meeting link approvals """
    meeting_title = models.CharField(max_length=200)
    scheduled_datetime = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    agenda = models.TextField(blank=True, null=True)
    
    # Handled by IT Administrator post-approval
    generated_zoom_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Zoom Request: {self.meeting_title}"