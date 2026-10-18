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
    
    # Dashboards
    path('dashboard/student/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/instructor/', views.InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('dashboard/visiting-faculty/', views.VisitingFacultyDashboardView.as_view(), name='visiting_faculty_dashboard'),
    path('dashboard/hod/', views.HODDashboardView.as_view(), name='hod_dashboard'),
    path('dashboard/accountant/', views.AccountantDashboardView.as_view(), name='accountant_dashboard'),
    path('dashboard/admissions/', views.AdmissionsDashboardView.as_view(), name='admissions_dashboard'),
    
    # o
    path('voucher/<int:voucher_id>/verify/', views.VerifyVoucherPaymentView.as_view(), name='verify_voucher_payment'),
    path('challan/<int:enrollment_id>/download/', views.DownloadChallanView.as_view(), name='download_challan'),
    path('student/upload-documents/', views.UploadStudentDocumentsView.as_view(), name='upload_student_documents'),
    path('admissions/verify/<int:student_id>/', views.VerifyStudentDocumentView.as_view(), name='verify_student_document'),
    path('discussions/', views.DiscussionBoardView.as_view(), name='discussion_board'),
    path('discussions/topic/<int:pk>/', views.DiscussionTopicDetailView.as_view(), name='discussion_topic_detail'),
    path('discussions/topic/<int:topic_id>/comment/', views.AddDiscussionCommentView.as_view(), name='add_discussion_comment'),
    path('discussions/create/', views.CreateDiscussionTopicView.as_view(), name='create_discussion_topic'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/toggle-complete/', views.ToggleLessonCompleteView.as_view(), name='toggle_lesson_complete'),
    path('session/create/', views.CreateLiveSessionView.as_view(), name='create_live_session'),
    path('live/<int:session_id>/', views.LiveSessionRoomView.as_view(), name='live_session_room'),
    path('quizzes/<int:pk>/take/', views.QuizTakeView.as_view(), name='quiz_take'),
    path('quizzes/<int:pk>/latest-result/', views.LatestQuizResultRedirectView.as_view(), name='quiz_result_latest'),
    path('quiz-attempts/<int:pk>/', views.QuizResultDetailView.as_view(), name='quiz_result_detail'),
    path('faculty/claims/', views.VisitingFacultyClaimEngineView.as_view(), name='faculty_claims'),
    path('hod/sections/', views.HODSectionAssignmentView.as_view(), name='hod_section_assignment'),
    path('hod/claims/<int:claim_id>/approve/', views.HODApproveClaimView.as_view(), name='approve_claim'),
    path('hod/invite-faculty/', views.InviteFacultyView.as_view(), name='invite_faculty'),
    path('api/ai-assistant/', views.AIChatAssistantView.as_view(), name='ai_assistant_api'),
    path('certificates/<uuid:certificate_id>/download/', views.DownloadCertificatePillowView.as_view(), name='download_certificate'),
]