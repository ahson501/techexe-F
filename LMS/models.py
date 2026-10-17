import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

class TimeStampedModel(models.Model):
    """Abstract base model adding created_at and updated_at timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStampedModel):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        INSTRUCTOR = 'INSTRUCTOR', 'Faculty / Instructor'
        VISITING_FACULTY = 'VISITING', 'Visiting Faculty'
        ADMISSIONS_OFFICER = 'ADMISSIONS', 'Admissions Officer'
        ACCOUNTANT = 'ACCOUNTANT', 'Accountant'
        HOD = 'HOD', 'Head of Department'
        ORG_ADMIN = 'ORG_ADMIN', 'Organization Admin'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lms_profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone_number = models.CharField(max_length=20, blank=True)
    cnic_or_bform = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=150, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    bank_account_info = models.TextField(blank=True, help_text="Bank details for visiting faculty claims.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    

# ==========================================
# 1. FACULTY INVITATION & PROFILE WORKFLOW
# ==========================================

class FacultyInvitation(TimeStampedModel):
    """Invited by Admin/HOD. Faculty accounts are created by invitation only."""
    class FacultyType(models.TextChoices):
        PERMANENT = 'PERMANENT', 'Permanent Faculty'
        VISITING = 'VISITING', 'Visiting Faculty'

    class Status(models.TextChoices):
        INVITED = 'INVITED', 'Invited'
        PROFILE_SUBMITTED = 'SUBMITTED', 'Profile Submitted'
        APPROVED = 'APPROVED', 'Approved'
        ACTIVE = 'ACTIVE', 'Active'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        CONTRACT_ENDED = 'CONTRACT_ENDED', 'Contract Ended'

    email = models.EmailField(unique=True)
    department = models.CharField(max_length=150)
    faculty_type = models.CharField(max_length=20, choices=FacultyType.choices, default=FacultyType.PERMANENT)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INVITED)
    
    # Extended verification profile fields
    cnic_or_passport = models.CharField(max_length=30, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    bank_details = models.TextField(blank=True, help_text="Bank details for visiting faculty claims processing.")
    documents = models.FileField(upload_to='faculty_docs/', blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='faculty_invitation')

    def __str__(self):
        return f"{self.email} ({self.faculty_type}) - {self.status}"


# ==========================================
# 2. COURSE STRUCTURE MODELS
# ==========================================

class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_teaching')
    
    # Prerequisites
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='prerequisite_for')
    
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class CourseSection(TimeStampedModel):
    """Course section assigned by HOD to faculty members."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100, help_text="e.g. Section A, Batch 2026")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_sections')
    confirmed_by_faculty = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - {self.name} ({self.instructor.get_full_name() or self.instructor.username})"


class Module(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = RichTextUploadingField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"


class Lesson(TimeStampedModel):
    class ContentType(models.TextChoices):
        VIDEO = 'VIDEO', 'Video Lecture'
        TEXT = 'TEXT', 'Text / Article'
        PDF = 'PDF', 'PDF Resource'

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=ContentType.choices, default=ContentType.TEXT)
    
    # Content Fields
    body_text = RichTextUploadingField(blank=True, null=True, help_text="Used for text articles or lecture transcripts.")
    video_url = models.URLField(blank=True, help_text="HLS stream URL or Cloudflare/AWS video URL.")
    pdf_file = models.FileField(upload_to='course_pdfs/', blank=True, null=True)
    
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=1)
    is_preview = models.BooleanField(default=False, help_text="Allow non-enrolled users to view for free.")

    class Meta:
        ordering = ['order']
        unique_together = ('module', 'order')

    def __str__(self):
        return f"{self.module.title} - Lesson {self.order}: {self.title}"


# ==========================================
# 3. QUIZ & ASSESSMENT MODELS
# ==========================================

class Quiz(TimeStampedModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    pass_mark_percentage = models.PositiveIntegerField(
        default=70, 
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    time_limit_minutes = models.PositiveIntegerField(default=0, help_text="0 means no time limit.")
    max_attempts = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"Quiz: {self.title} ({self.module.title})"


class Question(TimeStampedModel):
    class QuestionType(models.TextChoices):
        SINGLE_CHOICE = 'SINGLE', 'Single Choice (Radio)'
        MULTIPLE_CHOICE = 'MULTIPLE', 'Multiple Choice (Checkbox)'
        TRUE_FALSE = 'TRUE_FALSE', 'True / False'

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QuestionType.choices, default=QuestionType.SINGLE_CHOICE)
    points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"


class AnswerChoice(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:30]} -> {self.text} ({'Correct' if self.is_correct else 'Wrong'})"


# ==========================================
# 4. ADMISSIONS, ENROLLMENT & PAYMENT WORKFLOW
# ==========================================

class AdmissionsApproval(TimeStampedModel):
    """Admissions Officer approval record for CNIC and qualifications."""
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Approval'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admissions_approval')
    cnic_or_bform = models.CharField(max_length=30)
    qualification_document = models.FileField(upload_to='admissions_docs/')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admissions_officer')

    def __str__(self):
        return f"Admissions {self.student.username} - {self.status}"


class Voucher(TimeStampedModel):
    """Voucher created per course order with 7-day default validity."""
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Pending Payment'
        PAID = 'PAID', 'Paid'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vouchers')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='vouchers')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timezone.timedelta(days=7) # 7-day voucher validity rule
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.due_date and self.status == self.Status.OPEN

    def __str__(self):
        return f"Voucher {str(self.id)[:8]} - {self.student.username} ({self.status})"


class ChallanPayment(TimeStampedModel):
    """Manual bank challan or online payment receipt verification."""
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Verification'
        APPROVED = 'APPROVED', 'Approved by Accountant'
        REJECTED = 'REJECTED', 'Rejected'

    voucher = models.OneToOneField(Voucher, on_delete=models.CASCADE, related_name='payment')
    receipt_file = models.FileField(upload_to='payment_receipts/', blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.TextField(blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accountant_verifier')

    def __str__(self):
        return f"Payment Voucher {str(self.voucher.id)[:8]} - {self.status}"


class Enrollment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Payment'
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        EXPIRED = 'EXPIRED', 'Expired'
        CANCELLED = 'CANCELLED', 'Cancelled'
        REFUNDED = 'REFUNDED', 'Refunded'

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title} ({self.status})"


class LessonProgress(TimeStampedModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"{self.student.username} - {self.lesson.title}: {status}"


class QuizAttempt(TimeStampedModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    passed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} (Attempt #{self.attempt_number}: {self.score_percentage}%)"


# ==========================================
# 5. CERTIFICATE
# ==========================================

class Certificate(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_code = models.CharField(max_length=50, unique=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def save(self, *args, **kwargs):
        if not self.certificate_code:
            self.certificate_code = f"CERT-{self.issued_at.year if self.issued_at else '2026'}-{str(self.id)[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate for {self.student.username} - {self.course.title}"


# ==========================================
# 6. LIVE SESSIONS & FACULTY CLAIMS WORKFLOW
# ==========================================

class LiveSession(TimeStampedModel):
    class Mode(models.TextChoices):
        ONLINE = 'ONLINE', 'Online (Jitsi Stream)'
        PHYSICAL = 'PHYSICAL', 'Physical Campus'
        HYBRID = 'HYBRID', 'Hybrid (Room + Online)'

    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        HELD = 'HELD', 'Held / In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        RESCHEDULED = 'RESCHEDULED', 'Rescheduled'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_sessions')
    section = models.ForeignKey(CourseSection, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    title = models.CharField(max_length=255)
    description = RichTextUploadingField(blank=True, null=True)
    mode = models.CharField(max_length=10, choices=Mode.choices, default=Mode.ONLINE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.SCHEDULED)
    
    # Campus Details
    campus_room = models.CharField(max_length=100, blank=True, help_text="Used for physical/hybrid sessions.")
    
    # Scheduling
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    
    # Meeting URLs & Access
    join_url = models.URLField(max_length=500, blank=True, help_text="Instructor or Student Join Link")
    recording_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link to session recording")

    def is_live(self):
        now = timezone.now()
        end_time = self.start_time + timezone.timedelta(minutes=self.duration_minutes)
        return self.start_time <= now <= end_time and self.status in [self.Status.SCHEDULED, self.Status.HELD]  # ✅ Lowercase 'self'

    def __str__(self):
        return f"{self.course.title} - {self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"


class SessionAttendance(TimeStampedModel):
    """Online join log or physical QR code attendance log."""
    class ModeJoined(models.TextChoices):
        ONLINE = 'ONLINE', 'Joined Online'
        PHYSICAL = 'PHYSICAL', 'Attended Physical Class'

    session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_attendances')
    attended = models.BooleanField(default=True)
    joined_via = models.CharField(max_length=10, choices=ModeJoined.choices, default=ModeJoined.ONLINE)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.session.title} ({self.joined_via})"

# ==========================================
# 7. GROUP DISCUSSION & CLASS FORUMS
# ==========================================

class DiscussionTopic(TimeStampedModel):
    """Forum topics created by faculty or students for course/section discussions."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussion_topics')
    section = models.ForeignKey(CourseSection, on_delete=models.SET_NULL, null=True, blank=True, related_name='discussion_topics', help_text="Optional: Restrict discussion to a specific section/batch.")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_topics')
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    
    # Moderation & Visibility
    is_pinned = models.BooleanField(default=False, help_text="Pin topic to top of discussion board.")
    is_closed = models.BooleanField(default=False, help_text="Close topic to prevent new replies.")

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"[{self.course.title}] {self.title} by {self.author.username}"


class DiscussionPost(TimeStampedModel):
    """Replies and nested comments within a discussion topic."""
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_posts')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', help_text="Supports nested thread replies.")
    content = RichTextUploadingField()
    is_instructor_response = models.BooleanField(default=False, help_text="Highlights response from permanent or visiting faculty.")

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        # Auto-detect if post is from an instructor or staff
        if self.author.groups.filter(name='LMS_Instructor').exists() or self.author.is_staff:
            self.is_instructor_response = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reply by {self.author.username} on '{self.topic.title}'"

class DiscussionComment(models.Model):
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.topic.title}"

class VisitingFacultyClaim(TimeStampedModel):
    """Claim built from completed sessions for visiting faculty payment."""
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        HOD_APPROVED = 'APPROVED', 'HOD Approved'
        PAID = 'PAID', 'Paid'
        REJECTED = 'REJECTED', 'Rejected'

    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faculty_claims')
    sessions = models.ManyToManyField(LiveSession, related_name='claims')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.DRAFT)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_claims')

    def __str__(self):
        return f"Claim #{self.id} - {self.faculty.username} ({self.status})"