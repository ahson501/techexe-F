from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LessonProgress, Enrollment, Certificate, Lesson

@receiver(post_save, sender=LessonProgress)
def check_course_completion(sender, instance, **kwargs):
    """Triggers whenever a lesson is marked completed. Generates certificate if 100% complete."""
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

    # If all lessons are completed, mark enrollment as complete & create certificate
    if completed_lessons >= total_lessons:
        enrollment, _ = Enrollment.objects.get_or_create(student=student, course=course)
        if not enrollment.completed:
            enrollment.completed = True
            enrollment.save()

        # Generate Certificate entry if missing
        Certificate.objects.get_or_create(student=student, course=course)