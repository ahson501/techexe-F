from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import (
    Category, Course, Module, Lesson, Quiz,LiveSession, 
    Question, AnswerChoice, Enrollment, LessonProgress, QuizAttempt, Certificate
)
from .models import DiscussionTopic, DiscussionPost

# ==========================================
# 1. INLINES FOR FAST NESTED EDITING
# ==========================================

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('title', 'content_type', 'order', 'is_preview', 'duration_minutes')
        }),
        ('Content Details', {
            'classes': ('collapse',),
            'fields': ('body_text', 'video_url', 'pdf_file'),
        }),
    )


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    show_change_link = True
    fields = ('order', 'title')


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


# ==========================================
# 2. MAIN LMS MODEL ADMINS
# ==========================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'course_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_course_count=Count('courses'))

    @admin.display(description='Total Courses', ordering='_course_count')
    def course_count(self, obj):
        return obj._course_count


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'status_badge', 'price', 'enrolled_students', 'created_at')
    list_filter = ('status', 'is_featured', 'category', 'created_at')
    search_fields = ('title', 'description', 'instructor__username', 'instructor__email')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('prerequisites',)
    inlines = [ModuleInline]
    actions = ['make_published', 'make_draft']

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'DRAFT': '#6c757d',
            'PUBLISHED': '#28a745',
            'ARCHIVED': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_enrolled_students=Count('enrollments', distinct=True))

    @admin.display(description='Enrolled Students', ordering='_enrolled_students')
    def enrolled_students(self, obj):
        return obj._enrolled_students

    # Custom Admin Actions
    @admin.action(description="Mark selected courses as Published")
    def make_published(self, request, queryset):
        queryset.update(status=Course.Status.PUBLISHED)

    @admin.action(description="Mark selected courses as Draft")
    def make_draft(self, request, queryset):
        queryset.update(status=Course.Status.DRAFT)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'lesson_count')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_lesson_count=Count('lessons'))

    @admin.display(description='Lessons', ordering='_lesson_count')
    def lesson_count(self, obj):
        return obj._lesson_count


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'content_type', 'duration_minutes', 'order', 'is_preview')
    list_filter = ('content_type', 'is_preview', 'module__course')
    search_fields = ('title', 'body_text', 'module__title')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'pass_mark_percentage', 'max_attempts', 'time_limit_minutes')
    list_filter = ('module__course',)
    search_fields = ('title', 'module__title')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_truncated', 'quiz', 'question_type', 'points')
    list_filter = ('question_type', 'quiz__module__course')
    search_fields = ('text', 'quiz__title')
    inlines = [AnswerChoiceInline]

    @admin.display(description='Question Text')
    def text_truncated(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text


# ==========================================
# 3. ENROLLMENT & PROGRESS TRACKING ADMINS
# ==========================================

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'completed', 'created_at', 'completion_date')
    list_filter = ('completed', 'course')
    search_fields = ('student__username', 'student__email', 'course__title')
    raw_id_fields = ('student', 'course')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'is_completed', 'last_viewed_at')
    list_filter = ('is_completed', 'lesson__module__course')
    search_fields = ('student__username', 'lesson__title')
    raw_id_fields = ('student', 'lesson')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score_percentage', 'passed_badge', 'attempt_number', 'created_at')
    list_filter = ('passed', 'quiz__module__course')
    search_fields = ('student__username', 'quiz__title')
    raw_id_fields = ('student', 'quiz')

    @admin.display(description='Status')
    def passed_badge(self, obj):
        color = '#28a745' if obj.passed else '#dc3545'
        label = 'PASSED' if obj.passed else 'FAILED'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">{}</span>',
            color, label
        )


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    # Change 'platform' to 'mode'
    list_display = ('title', 'course', 'section', 'start_time', 'mode', 'status')
    list_filter = ('mode', 'status', 'course')
    search_fields = ('title', 'course__title', 'campus_room')

@admin.register(DiscussionTopic)
class DiscussionTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'section', 'author', 'is_pinned', 'is_closed', 'created_at')
    list_filter = ('is_pinned', 'is_closed', 'course')
    search_fields = ('title', 'content', 'author__username')

@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'is_instructor_response', 'created_at')
    list_filter = ('is_instructor_response', 'created_at')
    search_fields = ('content', 'author__username')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_code', 'student', 'course', 'issued_at')
    search_fields = ('certificate_code', 'student__username', 'course__title')
    list_filter = ('issued_at', 'course')