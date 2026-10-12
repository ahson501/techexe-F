from django.urls import path
from . import views


urlpatterns = [
    # Default index routes loading the Course List
    path('', views.CourseListView.as_view(), name='lms_index'),
    path('lessons/', views.CourseListView.as_view(), name='lessons_index'),

    # Existing routes
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<slug:slug>/enroll/', views.EnrollCourseView.as_view(), name='enroll_course'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/toggle-complete/', views.ToggleLessonCompleteView.as_view(), name='toggle_lesson_complete'),
    path('live/<int:session_id>/', views.LiveSessionRoomView.as_view(), name='live_session_room'),
    path('quizzes/<int:pk>/take/', views.QuizTakeView.as_view(), name='quiz_take'),
    path('quizzes/<int:pk>/latest-result/', views.LatestQuizResultRedirectView.as_view(), name='quiz_result_latest'),
    path('quiz-attempts/<int:pk>/', views.QuizResultDetailView.as_view(), name='quiz_result_detail'),
    path('api/ai-assistant/', views.AIChatAssistantView.as_view(), name='ai_assistant_api'),
    path('certificates/<uuid:certificate_id>/download/', views.DownloadCertificatePillowView.as_view(), name='download_certificate'),
]