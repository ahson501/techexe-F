from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    LessonProgress, Enrollment, Certificate, Lesson,
    SessionAttendance, LiveSession, DiscussionPost  # Replace DiscussionPost with your board model name if different
)

@receiver(post_save, sender=LessonProgress)
def check_course_completion(sender, instance, **kwargs):
    """Triggers whenever a lesson is marked completed. Marks attendance & generates certificate if 100% complete."""
    if not instance.is_completed:
        return

    student = instance.student
    course = instance.lesson.module.course

    # Count total lessons in course
    total_lessons = Lesson.objects.filter(module__course=course).count()
    if total_lessons == 0:
        return

    # Count completed lessons by student
    completed_lessons = LessonProgress.objects.filter(
        student=student,
        lesson__module__course=course,
        is_completed=True
    ).count()

    # If all lessons are completed, mark enrollment complete, mark attendance & create certificate
    if completed_lessons >= total_lessons:
        enrollment, _ = Enrollment.objects.get_or_create(student=student, course=course)
        if not enrollment.completed:
            enrollment.completed = True
            enrollment.save()

        # 1. NEW: Auto-mark attendance for all sessions in this course
        sessions = LiveSession.objects.filter(course=course)
        for session in sessions:
            SessionAttendance.objects.update_or_create(
                student=student,
                session=session,
                defaults={'attended': True}
            )

        # 2. Generate Certificate entry if missing (uses VLC-CERT-[Year]-[RegNo] in Certificate.save())
        Certificate.objects.get_or_create(student=student, course=course)


@receiver(post_save, sender=Lesson)
def notify_students_new_lesson(sender, instance, created, **kwargs):
    """Sends email to all enrolled students when an instructor adds a new lesson."""
    if created:
        course = instance.module.course
        enrolled_emails = list(
            Enrollment.objects.filter(course=course, status__in=['PAID', 'ACTIVE'])
            .values_list('student__email', flat=True)
        )
        enrolled_emails = [email for email in enrolled_emails if email]
        if enrolled_emails:
            send_mail(
                subject=f"New Lesson Added: {instance.title} ({course.title})",
                message=f"Hello,\n\nA new lesson '{instance.title}' has been added to {course.title}. Log in to view it.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=enrolled_emails,
                fail_silently=True,
            )


@receiver(post_save, sender=DiscussionPost)
def notify_students_announcement(sender, instance, created, **kwargs):
    """Sends email to enrolled students when an instructor posts an announcement."""
    if created and getattr(instance, 'is_announcement', True):
        author = instance.author
        is_faculty = author.groups.filter(
            name__in=['LMS_Instructor', 'LMS_VisitingFaculty', 'LMS_HOD']
        ).exists() or author.is_staff

        if is_faculty:
            enrolled_emails = list(
                Enrollment.objects.filter(course=instance.course, status__in=['PAID', 'ACTIVE'])
                .values_list('student__email', flat=True)
            )
            enrolled_emails = [email for email in enrolled_emails if email]
            if enrolled_emails:
                send_mail(
                    subject=f"Course Announcement: {instance.course.title}",
                    message=f"Instructor {author.get_full_name() or author.username} posted an announcement:\n\n{instance.content}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=enrolled_emails,
                    fail_silently=True,
                )