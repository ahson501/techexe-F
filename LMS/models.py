import uuid
from django.db import models
from django.conf import UserSettingsHolder
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField # Supports image/file uploads inline

User = get_user_model()


class TimeStampedModel(models.Model):
    """Abstract base model adding created_at and updated_at timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ==========================================
# 1. COURSE STRUCTURE MODELS
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
# 2. QUIZ & ASSESSMENT MODELS
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
# 3. USER ENROLLMENT & PROGRESS TRACKING
# ==========================================

class Enrollment(TimeStampedModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


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
# 4. CERTIFICATE
# ==========================================

class Certificate(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_code = models.CharField(max_length=50, unique=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def save(self, *args, **kwargs):
        if not self.certificate_code:
            # Generate readable verification code: CERT-YYYY-XXXX
            self.certificate_code = f"CERT-{self.issued_at.year if self.issued_at else '2026'}-{str(self.id)[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate for {self.student.username} - {self.course.title}"
    
 
# ==========================================
# 5. LIVE SESSIONS
# ==========================================

from django.utils import timezone
from .models import Course

class LiveSession(models.Model):
    PLATFORM_CHOICES = [
        ('ZOOM', 'Zoom Meeting'),
        ('JITSI', 'Jitsi Meet (Self-Hosted)'),
        ('BBB', 'BigBlueButton'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_sessions')
    title = models.CharField(max_length=255)
    description = RichTextUploadingField(blank=True, null=True)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, default='JITSI')
    
    # Scheduling
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    
    # Meeting URLs & Access
    join_url = models.URLField(max_length=500, help_text="Instructor or Student Join Link")
    recording_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link to session recording")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def is_live(self):
        now = timezone.now()
        end_time = self.start_time + timezone.timedelta(minutes=self.duration_minutes)
        return self.start_time <= now <= end_time

    def __str__(self):
        return f"{self.course.title} - {self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"