from django.conf import settings
from django.core.mail import send_mass_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from .models import (
    Certificate,
    DiscussionTopic,
    Enrollment,
    Lesson,
    LessonProgress,
    LiveSession,
    SessionAttendance,
)


def _send_course_notification(course, subject, build_body):
    """Sends individualized emails to all actively enrolled students in a course."""
    if not course:
        return

    enrollments = (
        Enrollment.objects.filter(
            course=course,
            status__in=[
                Enrollment.Status.ACTIVE,
                Enrollment.Status.COMPLETED,
                'PAID',
            ],
            student__is_active=True,
        )
        .exclude(student__email__isnull=True)
        .exclude(student__email__exact='')
        .select_related('student')
        .distinct()
    )

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'nsninsaan@gmail.com')
    messages = []
    seen_emails = set()

    for enrollment in enrollments:
        email = enrollment.student.email.strip()
        if not email or email in seen_emails:
            continue
        seen_emails.add(email)
        body = build_body(enrollment.student)
        messages.append((subject, body, from_email, [email]))

    if messages:
        try:
            send_mass_mail(tuple(messages), fail_silently=True)
        except Exception:
            pass


@receiver(post_save, sender=LessonProgress)
def check_course_completion(sender, instance, created, **kwargs):
    """Automatically updates enrollment status to COMPLETED and issues a Certificate when all lessons finish."""
    if not instance.is_completed:
        return

    enrollment = instance.enrollment
    course = enrollment.course
    total_lessons = Lesson.objects.filter(module__course=course).count()

    if total_lessons == 0:
        return

    completed_lessons = LessonProgress.objects.filter(
        enrollment=enrollment,
        is_completed=True,
    ).count()

    if completed_lessons >= total_lessons and enrollment.status != Enrollment.Status.COMPLETED:
        enrollment.status = Enrollment.Status.COMPLETED
        enrollment.completed_at = timezone.now()
        enrollment.save(update_fields=['status', 'completed_at'])

        Certificate.objects.get_or_create(
            student=enrollment.student,
            course=course,
        )


@receiver(post_save, sender=SessionAttendance)
def mark_attendance_on_join(sender, instance, created, **kwargs):
    """Ensures joining a live session is recorded as present."""
    if created and not instance.attended:
        instance.attended = True
        instance.save(update_fields=['attended'])


@receiver(post_save, sender=Lesson)
def notify_students_new_lesson(sender, instance, created, **kwargs):
    """Sends an individual email to active enrolled students when a new lesson is published."""
    if not created:
        return

    module = getattr(instance, 'module', None)
    course = getattr(module, 'course', None)
    if not course:
        return

    site_url = getattr(settings, 'SITE_URL', 'http://techexe.net').rstrip('/')
    try:
        course_path = reverse('course_detail', kwargs={'slug': course.slug})
    except Exception:
        course_path = f"/LMS/courses/{course.slug}/"
    course_url = f"{site_url}{course_path}"

    subject = f"New Lesson Added: {instance.title} ({course.title})"

    def build_body(student):
        name = student.get_full_name() or student.username
        module_line = f"Module: {module.title}\n" if getattr(module, 'title', None) else ""
        return (
            f"Hello {name},\n\n"
            f"A new lesson has been added to your course \"{course.title}\":\n\n"
            f"{module_line}"
            f"Lesson: {instance.title}\n\n"
            f"Access the lesson here:\n{course_url}\n\n"
            f"Best regards,\n"
            f"TechExe Academic Management\n"
        )

    _send_course_notification(course, subject, build_body)


@receiver(post_save, sender=DiscussionTopic)
def notify_students_discussion_announcement(sender, instance, created, **kwargs):
    """Sends an individual email to active enrolled students when faculty/HOD posts a discussion topic."""
    if not created:
        return

    author = instance.author
    is_faculty_or_hod = (
        author.is_staff
        or author.is_superuser
        or author.groups.filter(
            name__in=['LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD', 'LMS_admissions_officer']
        ).exists()
    )
    if not is_faculty_or_hod or not instance.course:
        return

    course = instance.course
    author_name = author.get_full_name() or author.username
    clean_body = strip_tags(instance.content or '').strip()
    subject = f"Course Announcement: {instance.title} ({course.title})"

    site_url = getattr(settings, 'SITE_URL', 'http://techexe.net').rstrip('/')
    try:
        topic_path = reverse('discussion_topic_detail', kwargs={'pk': instance.pk})
    except Exception:
        topic_path = '/LMS/discussion/'
    topic_url = f"{site_url}{topic_path}"

    def build_body(student):
        name = student.get_full_name() or student.username
        return (
            f"Hello {name},\n\n"
            f"{author_name} posted a new announcement in \"{course.title}\":\n\n"
            f"Topic: {instance.title}\n\n"
            f"{clean_body}\n\n"
            f"View and reply on the Class Discussion Board:\n"
            f"{topic_url}\n\n"
            f"Best regards,\n"
            f"TechExe Academic Management\n"
        )

    _send_course_notification(course, subject, build_body)